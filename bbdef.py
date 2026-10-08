import pandas as pd
import random
from baseprobabilities import *


ALL_PLAYERS = [
    "g1", "g2", "g3", "g4", "g5", "g6",
    "f1", "f2", "f3", "f4", "f5", "f6",
    "c1", "c2", "c3",
]

GUARD_PLAYERS = [
    "g1", "g2", "g3", "g4", "g5", "g6",
]

FORWARD_PLAYERS = [
    "f1", "f2", "f3", "f4", "f5", "f6",
]

CENTER_PLAYERS = [
    "c1", "c2", "c3",
]

PRIMARY_DEFENDER_WEIGHT = 0.70
SAME_POSITION_DEFENDER_WEIGHT = 0.20
HELP_DEFENDER_WEIGHT = 0.10


def getPlayers(t1_lineups,t2_lineups):
    """
    Return college-lineup player assignments and usage weights.

    Example:
        t1Players["g1"]["ID"] -> player ID
        t1Players["g1"]["usage"] -> usage weight
    """

    if t1_lineups.empty:
        raise ValueError("Team 1 college lineup is empty.")

    if t2_lineups.empty:
        raise ValueError("Team 2 college lineup is empty.")

    requiredColumns = ["id","position","first_string_id","fs_minutes","fs_inside_proportion","fs_mid_proportion","fs_three_proportion","second_string_id","ss_minutes","ss_inside_proportion","ss_mid_proportion","ss_three_proportion","third_string_id","ts_minutes","ts_inside_proportion","ts_mid_proportion","ts_three_proportion"]
    missingT1 = [column for column in requiredColumns if column not in t1_lineups.columns]
    missingT2 = [column for column in requiredColumns if column not in t2_lineups.columns]

    if missingT1:
        raise ValueError(f"Team 1 college lineup is missing columns: {missingT1}")

    if missingT2:
        raise ValueError(f"Team 2 college lineup is missing columns: {missingT2}")

    def buildTeamPlayers(lineups):
        players = {slot:{"ID":None,"usage":0.0,"inside_preference":100 / 3,"midrange_preference":100 / 3,"three_preference":100 / 3} for slot in ALL_PLAYERS}
        stringColumns = [("first_string_id","fs_minutes","fs_inside_proportion","fs_mid_proportion","fs_three_proportion",0),("second_string_id","ss_minutes","ss_inside_proportion","ss_mid_proportion","ss_three_proportion",1),("third_string_id","ts_minutes","ts_inside_proportion","ts_mid_proportion","ts_three_proportion",2)]
        positionSettings = {"G":("g",2),"F":("f",2),"C":("c",1)}

        normalizedLineups = lineups.copy()
        normalizedLineups["position"] = normalizedLineups["position"].astype(str).str.upper().str.strip()

        for position,(slotPrefix,requiredRows) in positionSettings.items():
            positionRows = normalizedLineups[normalizedLineups["position"] == position].sort_values("id")

            if len(positionRows) != requiredRows:
                raise ValueError(f"College lineup requires {requiredRows} {position} row{'s' if requiredRows != 1 else ''}; found {len(positionRows)}.")

            for stringIndex,(playerColumn,usageColumn,insideColumn,midrangeColumn,threeColumn,stringOffset) in enumerate(stringColumns):
                for rowIndex,(_,lineupRow) in enumerate(positionRows.iterrows()):
                    slotNumber = (stringOffset * requiredRows) + rowIndex + 1
                    slot = f"{slotPrefix}{slotNumber}"
                    playerValue = lineupRow[playerColumn]
                    usageValue = lineupRow[usageColumn]

                    if pd.isna(playerValue):
                        playerId = None
                    else:
                        playerId = int(playerValue)

                    if pd.isna(usageValue):
                        usage = 0.0
                    else:
                        usage = max(0.0,float(usageValue))

                    rawPreferences = [lineupRow[insideColumn],lineupRow[midrangeColumn],lineupRow[threeColumn]]
                    preferences = [max(0.0,float(value)) if not pd.isna(value) else 0.0 for value in rawPreferences]
                    preferenceTotal = sum(preferences)
                    if preferenceTotal > 0:
                        preferences = [(preference / preferenceTotal) * 100 for preference in preferences]
                    else:
                        preferences = [100 / 3,100 / 3,100 / 3]

                    players[slot] = {"ID":playerId,"usage":usage,"inside_preference":preferences[0],"midrange_preference":preferences[1],"three_preference":preferences[2]}

        return players

    t1Players = buildTeamPlayers(t1_lineups)
    t2Players = buildTeamPlayers(t2_lineups)

    return t1Players, t2Players


def indexRoster(roster_df):
    """
    Index a roster DataFrame by player ID.
    """

    if "ID" not in roster_df.columns:
        raise ValueError(
            "Roster DataFrame does not contain an ID column."
        )

    if roster_df["ID"].isna().any():
        raise ValueError(
            "Roster DataFrame contains null ID values."
        )

    roster_df = roster_df.copy()
    roster_df["ID"] = roster_df["ID"].astype(int)

    if roster_df["ID"].duplicated().any():
        dupes = roster_df.loc[roster_df["ID"].duplicated(keep=False), "ID"].unique().tolist()
        raise ValueError(f"Roster DataFrame contains duplicate ID values: {dupes}")

    return roster_df.set_index("ID", drop=False)

def get_stamina_adjusted_rating(player,ratingName,minutesPlayed,recoveryMinutes=0.0):
    baseRating = float(player[ratingName])
    staminaCapacity = max(1.0,float(player["stamina"]))
    minutesPlayed = max(0.0,float(minutesPlayed))
    recoveryMinutes = max(0.0,float(recoveryMinutes))
    effectiveFatigueMinutes = max(0.0,minutesPlayed - recoveryMinutes)

    staminaUsageRatio = effectiveFatigueMinutes / staminaCapacity
    normalStaminaUsageRatio = min(1.0,staminaUsageRatio)
    excessStaminaUsageRatio = max(0.0,staminaUsageRatio - 1.0)

    fatiguePenalty = (staminaNormalMaximumPenalty * (normalStaminaUsageRatio ** 2)) + (staminaExcessPenaltyPerRatio * excessStaminaUsageRatio)
    staminaModifier = max(staminaMinimumModifier,1.0 - fatiguePenalty)
    effectiveRating = baseRating * staminaModifier

    return effectiveRating,baseRating,staminaCapacity,minutesPlayed,staminaUsageRatio,fatiguePenalty,staminaModifier


def weightedPlayerSelection(player_slots,team_players,roster_by_id,number_to_select,excluded_player_ids=None,already_selected_player_ids=None):
    """
    Select unique players from the supplied position group. If that group
    cannot fill every requested position, use any remaining game-plan player.
    """
    if excluded_player_ids is None:
        excluded_player_ids = set()
    if already_selected_player_ids is None:
        already_selected_player_ids = set()

    unavailablePlayerIds = {int(playerId) for playerId in excluded_player_ids}
    unavailablePlayerIds.update(int(playerId) for playerId in already_selected_player_ids)

    def buildEligiblePlayers(playerSlots,additionalUnavailablePlayerIds=None):
        if additionalUnavailablePlayerIds is None:
            additionalUnavailablePlayerIds = set()

        eligiblePlayers = []
        seenPlayerIds = set()

        for slot in playerSlots:
            playerId = team_players[slot]["ID"]
            usage = team_players[slot]["usage"]

            if playerId is None:
                continue

            playerId = int(playerId)

            if playerId == 0:
                continue

            if playerId in unavailablePlayerIds or playerId in additionalUnavailablePlayerIds or playerId in seenPlayerIds:
                continue

            if playerId not in roster_by_id.index:
                raise ValueError(f"Player ID {playerId} from slot {slot} was not found in the team roster.")

            eligiblePlayers.append({"slot": slot,"ID": playerId,"usage": max(0.0,float(usage)),})
            seenPlayerIds.add(playerId)

        return eligiblePlayers

    def selectWithoutReplacement(eligiblePlayers,selectionCount):
        selectedPlayers = []
        remainingPlayers = eligiblePlayers.copy()

        while len(selectedPlayers) < selectionCount and remainingPlayers:
            selectionWeights = [player["usage"] for player in remainingPlayers]

            if sum(selectionWeights) > 0:
                selectedPlayer = random.choices(remainingPlayers,weights=selectionWeights,k=1)[0]
            else:
                selectedPlayer = random.choice(remainingPlayers)

            selectedPlayers.append(selectedPlayer)
            selectedPlayerId = selectedPlayer["ID"]
            remainingPlayers = [player for player in remainingPlayers if player["ID"] != selectedPlayerId]

        return selectedPlayers

    primaryEligiblePlayers = buildEligiblePlayers(player_slots)
    primarySelectionCount = min(number_to_select,len(primaryEligiblePlayers))
    selectedPlayers = selectWithoutReplacement(primaryEligiblePlayers,primarySelectionCount)

    if len(selectedPlayers) < number_to_select:
        selectedPlayerIds = {player["ID"] for player in selectedPlayers}
        fallbackEligiblePlayers = buildEligiblePlayers(ALL_PLAYERS,selectedPlayerIds)
        fallbackSelectionCount = number_to_select - len(selectedPlayers)

        if len(fallbackEligiblePlayers) < fallbackSelectionCount:
            # Last resort: any non-excluded, non-selected player in the full roster.
            alreadyAccountedIds = unavailablePlayerIds | {int(p["ID"]) for p in selectedPlayers} | {int(p["ID"]) for p in fallbackEligiblePlayers}
            rosterFallbackIds = [rid for rid in roster_by_id.index if rid not in alreadyAccountedIds]
            if len(fallbackEligiblePlayers) + len(rosterFallbackIds) < fallbackSelectionCount:
                totalAvailablePlayers = len(selectedPlayers) + len(fallbackEligiblePlayers) + len(rosterFallbackIds)
                raise ValueError(f"Cannot select {number_to_select} players. Only {totalAvailablePlayers} eligible players remain after foul-out exclusions.")
            rosterFallbackNeeded = fallbackSelectionCount - len(fallbackEligiblePlayers)
            rosterFallbackChosen = random.sample(rosterFallbackIds, rosterFallbackNeeded)
            for rid in rosterFallbackChosen:
                fallbackEligiblePlayers.append({"slot": "roster_fallback", "ID": rid, "usage": 1.0})

        selectedPlayers.extend(selectWithoutReplacement(fallbackEligiblePlayers,fallbackSelectionCount))

    selectedRosterPlayers = []
    for player in selectedPlayers:
        rosterPlayer = roster_by_id.loc[player["ID"]].copy()
        sourceSlot = player["slot"]
        rosterPlayer["lineup_source_slot"] = sourceSlot
        if sourceSlot in team_players:
            rosterPlayer["inside_preference"] = team_players[sourceSlot]["inside_preference"]
            rosterPlayer["midrange_preference"] = team_players[sourceSlot]["midrange_preference"]
            rosterPlayer["three_preference"] = team_players[sourceSlot]["three_preference"]
        else:
            rosterPlayer["inside_preference"] = 100 / 3
            rosterPlayer["midrange_preference"] = 100 / 3
            rosterPlayer["three_preference"] = 100 / 3
        selectedRosterPlayers.append(rosterPlayer)

    return selectedRosterPlayers


def subPlayers(team_players,roster_by_id,forceStarters=False,excluded_player_ids=None,protected_player_id=None,protected_slot=None,protected_source_slot=None):
    """
    Return five players for the current lineup.

    Return order:
        guard 1, guard 2, forward 1, forward 2, center 1
    """
    if excluded_player_ids is None:
        excluded_player_ids = set()

    if forceStarters and not excluded_player_ids:
        starter_slots = [
            "g1",
            "g2",
            "f1",
            "f2",
            "c1",
        ]

        starters = []

        for slot in starter_slots:
            player_id = team_players[slot]["ID"]

            if player_id is None:
                raise ValueError(
                    f"Starter slot {slot} is empty."
                )

            if player_id not in roster_by_id.index:
                raise ValueError(
                    f"Starter player ID {player_id} from slot "
                    f"{slot} was not found in the roster."
                )

            starter = roster_by_id.loc[player_id].copy()
            starter["lineup_source_slot"] = slot
            starter["inside_preference"] = team_players[slot]["inside_preference"]
            starter["midrange_preference"] = team_players[slot]["midrange_preference"]
            starter["three_preference"] = team_players[slot]["three_preference"]
            starters.append(starter)

        return tuple(starters)

    if (protected_player_id is None) != (protected_slot is None):
        raise ValueError("Protected player ID and protected slot must be supplied together.")

    selectedLineup = {"g1":None,"g2":None,"f1":None,"f2":None,"c1":None}
    selectedPlayerIds = set()

    if protected_player_id is not None:
        protected_player_id = int(protected_player_id)
        if protected_slot not in selectedLineup:
            raise ValueError(f"Invalid protected lineup slot: {protected_slot}")
        if protected_player_id in excluded_player_ids:
            raise ValueError(f"Protected player ID {protected_player_id} is excluded from the lineup.")
        if protected_player_id not in roster_by_id.index:
            raise ValueError(f"Protected player ID {protected_player_id} was not found in the roster.")
        matchingSourceSlots = [slot for slot in ALL_PLAYERS if team_players[slot]["ID"] is not None and int(team_players[slot]["ID"]) == protected_player_id]
        protectedPlayer = roster_by_id.loc[protected_player_id].copy()
        if matchingSourceSlots:
            sourceSlot = protected_source_slot if protected_source_slot in matchingSourceSlots else max(matchingSourceSlots,key=lambda slot:team_players[slot]["usage"])
            protectedPlayer["lineup_source_slot"] = sourceSlot
            protectedPlayer["inside_preference"] = team_players[sourceSlot]["inside_preference"]
            protectedPlayer["midrange_preference"] = team_players[sourceSlot]["midrange_preference"]
            protectedPlayer["three_preference"] = team_players[sourceSlot]["three_preference"]
        else:
            # Roster fallback player (not in any lineup slot) who was brought in because too few lineup players were available.
            protectedPlayer["lineup_source_slot"] = "roster_fallback"
            protectedPlayer["inside_preference"] = 100 / 3
            protectedPlayer["midrange_preference"] = 100 / 3
            protectedPlayer["three_preference"] = 100 / 3
        selectedLineup[protected_slot] = protectedPlayer
        selectedPlayerIds.add(protected_player_id)

    openGuardSlots = [slot for slot in ["g1","g2"] if selectedLineup[slot] is None]
    openForwardSlots = [slot for slot in ["f1","f2"] if selectedLineup[slot] is None]
    openCenterSlots = [slot for slot in ["c1"] if selectedLineup[slot] is None]

    guards = weightedPlayerSelection(GUARD_PLAYERS,team_players,roster_by_id,len(openGuardSlots),excluded_player_ids,selectedPlayerIds)
    selectedPlayerIds.update(int(player["ID"]) for player in guards)

    forwards = weightedPlayerSelection(FORWARD_PLAYERS,team_players,roster_by_id,len(openForwardSlots),excluded_player_ids,selectedPlayerIds)
    selectedPlayerIds.update(int(player["ID"]) for player in forwards)

    centers = weightedPlayerSelection(CENTER_PLAYERS,team_players,roster_by_id,len(openCenterSlots),excluded_player_ids,selectedPlayerIds)

    for slot,player in zip(openGuardSlots,guards):
        selectedLineup[slot] = player
    for slot,player in zip(openForwardSlots,forwards):
        selectedLineup[slot] = player
    for slot,player in zip(openCenterSlots,centers):
        selectedLineup[slot] = player

    return selectedLineup["g1"],selectedLineup["g2"],selectedLineup["f1"],selectedLineup["f2"],selectedLineup["c1"]

def getOnCourtSlot(player, onCourt):
    """
    Return the lineup slot occupied by the supplied player Series.
    """

    player_id = int(player["ID"])

    for slot, on_court_player in onCourt.items():
        on_court_player_id = int(
            on_court_player["ID"]
        )

        if on_court_player_id == player_id:
            return slot

    return None


def selectDefender(
    poss_player,
    offense_on_court,
    defense_on_court,
    excluded_defender=None
):
    offense_slot = getOnCourtSlot(
        poss_player,
        offense_on_court
    )

    available_defenders = dict(defense_on_court)

    if excluded_defender is not None:
        excluded_defender_id = int(
            excluded_defender["id"]
        )

        available_defenders = {
            slot: player
            for slot, player in available_defenders.items()
            if int(player["id"]) != excluded_defender_id
        }

    if not available_defenders:
        raise ValueError(
            "No defenders are available for selection."
        )

    primary_defender = available_defenders.get(
        offense_slot
    )

    same_position_defenders = [
        player
        for player in available_defenders.values()
        if player["position"] == poss_player["position"]
        and (
            primary_defender is None
            or int(player["id"]) != int(primary_defender["id"])
        )
    ]

    help_defenders = [
        player
        for player in available_defenders.values()
        if (
            primary_defender is None
            or int(player["id"]) != int(primary_defender["id"])
        )
        and all(
            int(player["id"]) != int(same_position_player["id"])
            for same_position_player in same_position_defenders
        )
    ]

    selection_options = []
    selection_weights = []

    if primary_defender is not None:
        selection_options.append(primary_defender)
        selection_weights.append(70)

    if same_position_defenders:
        same_position_defender = random.choice(
            same_position_defenders
        )

        selection_options.append(
            same_position_defender
        )
        selection_weights.append(20)

    if help_defenders:
        help_defender = random.choice(
            help_defenders
        )

        selection_options.append(
            help_defender
        )
        selection_weights.append(10)

    if not selection_options:
        return random.choice(
            list(available_defenders.values())
        )

    return random.choices(
        selection_options,
        weights=selection_weights,
        k=1
    )[0]


def setLineups(t1Players,t2Players,t1RosterById,t2RosterById,t1Probabilities,t2Probabilities,HCAAdj,forceStarters=False,t1ExcludedPlayerIds=None,t2ExcludedPlayerIds=None,t1ProtectedPlayerId=None,t1ProtectedSlot=None,t2ProtectedPlayerId=None,t2ProtectedSlot=None,t1ProtectedSourceSlot=None,t2ProtectedSourceSlot=None):
    if t1ExcludedPlayerIds is None:
        t1ExcludedPlayerIds = set()
    if t2ExcludedPlayerIds is None:
        t2ExcludedPlayerIds = set()

    # Select the five players for each team.
    t1_selected = subPlayers(t1Players, t1RosterById, forceStarters, t1ExcludedPlayerIds, t1ProtectedPlayerId,t1ProtectedSlot,t1ProtectedSourceSlot)
    t2_selected = subPlayers(t2Players, t2RosterById, forceStarters, t2ExcludedPlayerIds, t2ProtectedPlayerId,t2ProtectedSlot,t2ProtectedSourceSlot)

    # Store each player by their current on-court slot.
    t1onCourt = {
        "g1": t1_selected[0],
        "g2": t1_selected[1],
        "f1": t1_selected[2],
        "f2": t1_selected[3],
        "c1": t1_selected[4],
    }

    t2onCourt = {
        "g1": t2_selected[0],
        "g2": t2_selected[1],
        "f1": t2_selected[2],
        "f2": t2_selected[3],
        "c1": t2_selected[4],
    }
    t1Rebound = sum(
        float((player["rebounding"])*100)
        for player in t1onCourt.values()
    )

    t2Rebound = sum(
        float((player["rebounding"])*100)
        for player in t2onCourt.values()
    )

    t1Ballwork = sum(
        float((player["ballwork"])*100)
        for player in t1onCourt.values()
    )

    t2Ballwork = sum(
        float((player["ballwork"])*100)
        for player in t2onCourt.values()
    )

    t1InsDef = sum(
        float((player["interior_defense"])*100)
        for player in t1onCourt.values()
    )

    t2InsDef = sum(
        float((player["interior_defense"])*100)
        for player in t2onCourt.values()
    )

    t1OutDef = sum(
        float((player["perimeter_defense"])*100)
        for player in t1onCourt.values()
    )

    t2OutDef = sum(
        float((player["perimeter_defense"])*100)
        for player in t2onCourt.values()
    )

    t1Def = sum(
        float(((player["interior_defense"]+player["perimeter_defense"])/2)*100)
        for player in t1onCourt.values()
    )

    t2Def = sum(
        float(((player["interior_defense"]+player["perimeter_defense"])/2)*100)
        for player in t2onCourt.values()
    )

    t1RebDiff = t1Rebound - t2Rebound
    t1BallDef = t1Ballwork - t2Def
    t1OffensiveRebound = round((0.00003 * t1RebDiff) + 0.28, 6)
    t1StealsAdj = round((-0.00000008 * t1BallDef), 6)
    t1OtherTO = round((-0.000005 * t1BallDef), 6)
    t1LooseBall = round((0.00003 * t1OffensiveRebound) + 0.28, 6)
    t1StealsAdjNeg = t1StealsAdj / (-3)
    t1OtherTOAdjNeg = t1OtherTO / (-3)
    t1BaseCutoff = 0
    t1StealCutoff = t1Probabilities["steal"] + t1StealsAdj + t1BaseCutoff
    t1TOCutoff = t1Probabilities["other_turnover"] + t1OtherTO + t1StealCutoff
    t1MoveCutoff = t1Probabilities["move"] + t1StealsAdjNeg + t1OtherTOAdjNeg + t1TOCutoff
    t1PassCutoff = t1Probabilities["pass"] + t1StealsAdjNeg + t1OtherTOAdjNeg + t1MoveCutoff
    t1ShotCutoff = t1Probabilities["shot"] + t1StealsAdjNeg + t1OtherTOAdjNeg + t1PassCutoff

    t2RebDiff = t2Rebound - t1Rebound
    t2BallDef = t2Ballwork - t1Def
    t2OffensiveRebound = round((0.00003 * t2RebDiff) + 0.28, 6)
    t2StealsAdj = round((-0.00000008 * t2BallDef), 6)
    t2OtherTO = round((-0.000005 * t2BallDef), 6)
    t2LooseBall = round((0.00003 * t2OffensiveRebound) + 0.28, 6)
    t2StealsAdjNeg = t2StealsAdj / (-3)
    t2OtherTOAdjNeg = t2OtherTO / (-3)
    t2BaseCutoff = 0
    t2StealCutoff = t2Probabilities["steal"] + t2StealsAdj + t2BaseCutoff
    t2TOCutoff = t2Probabilities["other_turnover"] + t2OtherTO + t2StealCutoff
    t2MoveCutoff = t2Probabilities["move"] + t2StealsAdjNeg + t2OtherTOAdjNeg + t2TOCutoff
    t2PassCutoff = t2Probabilities["pass"] + t2StealsAdjNeg + t2OtherTOAdjNeg + t2MoveCutoff
    t2ShotCutoff = t2Probabilities["shot"] + t2StealsAdjNeg + t2OtherTOAdjNeg + t2PassCutoff


    lineupParameters = {
        "t1Rebound": t1Rebound,
        "t1Ballwork": t1Ballwork,
        "t1RebDiff": t1RebDiff,
        "t1InsDef": t1InsDef,
        "t1OutDef": t1OutDef,
        "t1Def": t1Def,
        "t1BallDef": t1BallDef,
        "t1OffensiveRebound": t1OffensiveRebound,
        "t1StealsAdj": t1StealsAdj,
        "t1OtherTO": t1OtherTO,
        "t1LooseBall": t1LooseBall,
        "t1StealsAdjNeg": t1StealsAdjNeg,
        "t1OtherTOAdjNeg": t1OtherTOAdjNeg,
        "t1BaseCutoff": t1BaseCutoff,
        "t1StealCutoff": t1StealCutoff,
        "t1TOCutoff": t1TOCutoff,
        "t1MoveCutoff": t1MoveCutoff,
        "t1PassCutoff": t1PassCutoff,
        "t1ShotCutoff": t1ShotCutoff,

        "t2Rebound": t2Rebound,
        "t2Ballwork": t2Ballwork,
        "t2RebDiff": t2RebDiff,
        "t2InsDef": t2InsDef,
        "t2OutDef": t2OutDef,
        "t2Def": t2Def,
        "t2BallDef": t2BallDef,
        "t2OffensiveRebound": t2OffensiveRebound,
        "t2StealsAdj": t2StealsAdj,
        "t2OtherTO": t2OtherTO,
        "t2LooseBall": t2LooseBall,
        "t2StealsAdjNeg": t2StealsAdjNeg,
        "t2OtherTOAdjNeg": t2OtherTOAdjNeg,
        "t2BaseCutoff": t2BaseCutoff,
        "t2StealCutoff": t2StealCutoff,
        "t2TOCutoff": t2TOCutoff,
        "t2MoveCutoff": t2MoveCutoff,
        "t2PassCutoff": t2PassCutoff,
        "t2ShotCutoff": t2ShotCutoff,
    }

    return t1onCourt, t2onCourt, lineupParameters

def resolve_free_throw(shooter,homeCourtAdjustment,staminaModifier=1.0):
    baseFreeThrowRating = float(shooter["free_throw"])
    freeThrowRating = baseFreeThrowRating * staminaModifier
    baseFreeThrowChance = (ftMagicNum1 * freeThrowRating) + ftMagicNum2
    freeThrowChance = baseFreeThrowChance + homeCourtAdjustment
    freeThrowRoll = random.random()
    freeThrowMade = (freeThrowRoll < freeThrowChance)
    return freeThrowMade,freeThrowChance,freeThrowRoll,freeThrowRating,baseFreeThrowRating
