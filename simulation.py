import csv
import random
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import math

from baseprobabilities import *
from dbconn import *

from bbdef import *
from courtDef import *

def rungame(gid, home, away, league, HC, gamenum):
    t1 = home
    t2 = away

    if HC == 1:
        HCA = 0.005
    else:
        HCA = 0
    HCAAdj = round(HCA / 3, 12)

    gameType = league

    # Quarter Length (in seconds) - CBB 1200 / NBA 720
    # Number of Quarters per Half - CBB 1 / NBA 2
    # Shot Clock - CBB 30 (reset 20) / NBA 24 (reset 14)

    gameOn = True
    periodOn = True
    tipOff = True
    period = 1

    t1pts = 0
    t2pts = 0

    t1q1pts = 0
    t1q2pts = 0
    t1q3pts = 0
    t1q4pts = 0
    t1qotpts = 0

    t2q1pts = 0
    t2q2pts = 0
    t2q3pts = 0
    t2q4pts = 0
    t2qotpts = 0

    t13a = 0
    t13m = 0
    t12a = 0
    t12m = 0

    t23a = 0
    t23m = 0
    t22a = 0
    t22m = 0

    if gameType == "CBB":
        qtrTime = 1200
        otQtrTime = 300
        periodPerGame = 2
        shotClock = 30
        shotClockReset = 20
        pInd = "H"
        foulOutLimit = 5
    else:
        qtrTime = 700
        otQtrtime = 300
        periodPerGame = 4
        shotClock = 24
        shotClockReset = 14
        pInd = "Q"
        foulOutLimit = 6

    cbbMediaTimeoutMarks = [960,720,480,240]
    cbbMediaTimeoutsTaken = {periodNumber:set() for periodNumber in range(1,periodPerGame + 1)}
    nbaTimeoutEventsByPeriod = {periodNumber:0 for periodNumber in range(1,periodPerGame + 1)}

    currTime = qtrTime
    currShotClock = shotClock

    courtPos = (0,3)
    footerPos = ""
    crossed_midcourt = False

    t1p1pts = 0
    t1p2pts = 0
    t1p3pts = 0
    t1p4pts = 0
    t1otpts = 0

    t2p1pts = 0
    t2p2pts = 0
    t2p3pts = 0
    t2p4pts = 0
    t2otpts = 0

    t1pts = 0
    t2pts = 0
    fieldPos = 0

    t1StartChance = 0.5
    t2StartChance = 0.5

    t1RosterQuery = "SELECT * FROM college_players WHERE team_abbr = '%s'" % t1
    t1roster_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t1RosterQuery))

    t2RosterQuery = "SELECT * FROM college_players WHERE team_abbr = '%s'" % t2
    t2roster_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t2RosterQuery))

    t1FouledOutPlayerIds = set()
    t2FouledOutPlayerIds = set()

    t1FirstHalfTeamFouls = 0
    t1SecondHalfTeamFouls = 0
    t2FirstHalfTeamFouls = 0
    t2SecondHalfTeamFouls = 0

    t1stats = pd.DataFrame().assign(id=t1roster_df['player_id'], Team=t1roster_df['team_abbr'], FName=t1roster_df['first_name'], LName=t1roster_df['last_name'],Position=t1roster_df['position'])
    t2stats = pd.DataFrame().assign(id=t2roster_df['player_id'], Team=t2roster_df['team_abbr'], FName=t2roster_df['first_name'], LName=t2roster_df['last_name'],Position=t2roster_df['position'])

    t1stats['MP'] = 0.00
    t1stats['Assist'] = 0
    t1stats['Ins Shot Att'] = 0
    t1stats['Ins Shot Made'] = 0
    t1stats['Ins Shot %'] = 0
    t1stats['Mid Shot Att'] = 0
    t1stats['Mid Shot Made'] = 0
    t1stats['Mid Shot %'] = 0
    t1stats['3PT Shot Att'] = 0
    t1stats['3PT Shot Made'] = 0
    t1stats['3PT Shot %'] = 0
    t1stats['FT Shot Att'] = 0
    t1stats['FT Shot Made'] = 0
    t1stats['FT Shot %'] = 0
    t1stats['OREB'] = 0
    t1stats['DREB'] = 0
    t1stats['Stl'] = 0
    t1stats['Blk'] = 0
    t1stats['TO'] = 0
    t1stats['Foul'] = 0
    t1stats['Pts'] = 0
    t1stats.set_index('id', inplace=True)

    t2stats['MP'] = 0.00
    t2stats['Assist'] = 0
    t2stats['Ins Shot Att'] = 0
    t2stats['Ins Shot Made'] = 0
    t2stats['Ins Shot %'] = 0
    t2stats['Mid Shot Att'] = 0
    t2stats['Mid Shot Made'] = 0
    t2stats['Mid Shot %'] = 0
    t2stats['3PT Shot Att'] = 0
    t2stats['3PT Shot Made'] = 0
    t2stats['3PT Shot %'] = 0
    t2stats['FT Shot Att'] = 0
    t2stats['FT Shot Made'] = 0
    t2stats['FT Shot %'] = 0
    t2stats['OREB'] = 0
    t2stats['DREB'] = 0
    t2stats['Stl'] = 0
    t2stats['Blk'] = 0
    t2stats['TO'] = 0
    t2stats['Foul'] = 0
    t2stats['Pts'] = 0
    t2stats.set_index('id', inplace=True)

    t1TeamQuery = "SELECT * from college_teams where abbr = '%s'" % t1
    t2TeamQuery = "SELECT * from college_teams where abbr = '%s'" % t2
    t1team_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t1TeamQuery))
    t2team_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t2TeamQuery))
    t1id = t1team_df['id'].item()
    t2id = t2team_df['id'].item()

    t1LineupQuery = "SELECT * from college_lineups where team_id = '%s' AND deleted_at IS NULL ORDER BY id" % t1id
    t2LineupQuery = "SELECT * from college_lineups where team_id = '%s' AND deleted_at IS NULL ORDER BY id" % t2id
    t1Lineup_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t1LineupQuery))
    t2Lineup_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t2LineupQuery))
    t1GameplanQuery = "SELECT pace,offensive_formation,defensive_formation,focus_player,preserve_timeouts,trigger1_enabled,trigger1_type,trigger1_value,trigger2_enabled,trigger2_value,trigger3_enabled,trigger3_value,trigger3_exhaustion,trigger4_enabled,trigger4_value from college_gameplans where team_id = '%s' AND deleted_at IS NULL" % t1id
    t2GameplanQuery = "SELECT pace,offensive_formation,defensive_formation,focus_player,preserve_timeouts,trigger1_enabled,trigger1_type,trigger1_value,trigger2_enabled,trigger2_value,trigger3_enabled,trigger3_value,trigger3_exhaustion,trigger4_enabled,trigger4_value from college_gameplans where team_id = '%s' AND deleted_at IS NULL" % t2id
    t1Gameplan_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t1GameplanQuery))
    t2Gameplan_df = pd.read_sql_query(con=dbconn.connect(), sql=sql_text(t2GameplanQuery))

    if t1Gameplan_df.empty or t2Gameplan_df.empty:
        raise ValueError("Both teams require a college_gameplans record.")

    paceStaminaModifiers = {"Very Slow":1.15,"Slow":1.10,"Balanced":1.00,"Fast":0.90,"Very Fast":0.85}
    paceActionTimeModifiers = {"Very Slow":1.45,"Slow":1.25,"Balanced":1.00,"Fast":0.75,"Very Fast":0.55}
    paceActionTimeWeights = {"Very Slow":[50,25,15,7,3],"Slow":[25,40,25,8,2],"Balanced":[10,20,40,20,10],"Fast":[2,8,25,40,25],"Very Fast":[3,7,15,25,50]}
    paceShotClockUrgencyStarts = {"CBB":{"Very Slow":6.0,"Slow":8.0,"Balanced":10.0,"Fast":14.0,"Very Fast":18.0},"NBA":{"Very Slow":5.0,"Slow":7.0,"Balanced":10.0,"Fast":13.0,"Very Fast":16.0}}
    offensiveFormationDestinationWeights = {"Balanced":{"inside":1.00,"midrange":1.00,"three":1.00},"Motion":{"inside":1.06,"midrange":0.97,"three":1.04},"Pick-and-Roll":{"inside":1.08,"midrange":1.04,"three":0.94},"Post-Up":{"inside":1.12,"midrange":0.96,"three":0.90},"Space-and-Post":{"inside":0.94,"midrange":1.05,"three":1.10}}
    defensiveFormationDestinationWeights = {"Man-to-Man":{"inside":1.00,"midrange":1.00,"three":1.00},"1-3-1 Zone":{"inside":1.05,"midrange":0.92,"three":1.05},"3-2 Zone":{"inside":1.08,"midrange":1.02,"three":0.90},"2-3 Zone":{"inside":0.90,"midrange":1.02,"three":1.08},"Box-and-One Zone":{"inside":1.00,"midrange":1.00,"three":1.00}}
    lineupPreferenceNeutralShare = 100 / 3
    lineupPreferenceDestinationStrength = 0.35
    lineupPreferenceDestinationMinimum = 0.80
    lineupPreferenceDestinationMaximum = 1.20
    playerShotWillingnessPerProportionPoint = 0.0015
    playerShotWillingnessMaximumAdjustment = 0.03
    passReceiverPreferenceWeightPerProportionPoint = 0.015
    passReceiverPreferenceMinimumWeight = 0.65
    passReceiverPreferenceMaximumWeight = 1.35
    offensiveFormationReboundAdjustments = {"Balanced":0.000,"Motion":-0.005,"Pick-and-Roll":-0.005,"Post-Up":0.010,"Space-and-Post":-0.005}
    defensiveFormationOffensiveReboundAdjustments = {"Man-to-Man":0.000,"1-3-1 Zone":0.005,"3-2 Zone":0.005,"2-3 Zone":-0.010,"Box-and-One Zone":0.005}
    doubleTeamAdjustments = {"Man-to-Man":{"focus":{"shot":-0.020,"movement":-0.030,"pass_deflection":0.015},"teammate":{"shot":0.005,"movement":0.0075,"pass_deflection":-0.00375}},"Box-and-One Zone":{"focus":{"shot":-0.030,"movement":-0.040,"pass_deflection":0.020},"teammate":{"shot":0.0075,"movement":0.010,"pass_deflection":-0.005}}}
    t1Pace = str(t1Gameplan_df["pace"].iloc[0]).strip()
    t2Pace = str(t2Gameplan_df["pace"].iloc[0]).strip()
    if t1Pace not in paceStaminaModifiers or t2Pace not in paceStaminaModifiers:
        raise ValueError("Pace must be Very Slow, Slow, Balanced, Fast, or Very Fast.")
    t1PaceStaminaModifier = paceStaminaModifiers[t1Pace]
    t2PaceStaminaModifier = paceStaminaModifiers[t2Pace]
    t1OffensiveFormation = str(t1Gameplan_df["offensive_formation"].iloc[0] or "Balanced").strip()
    t2OffensiveFormation = str(t2Gameplan_df["offensive_formation"].iloc[0] or "Balanced").strip()
    t1DefensiveFormation = str(t1Gameplan_df["defensive_formation"].iloc[0] or "Man-to-Man").strip()
    t2DefensiveFormation = str(t2Gameplan_df["defensive_formation"].iloc[0] or "Man-to-Man").strip()
    t1FocusPlayerRaw = t1Gameplan_df["focus_player"].iloc[0]
    t2FocusPlayerRaw = t2Gameplan_df["focus_player"].iloc[0]
    t1FocusPlayerId = int(t1FocusPlayerRaw) if not pd.isna(t1FocusPlayerRaw) and str(t1FocusPlayerRaw).strip().isdigit() and int(t1FocusPlayerRaw) > 0 else None
    t2FocusPlayerId = int(t2FocusPlayerRaw) if not pd.isna(t2FocusPlayerRaw) and str(t2FocusPlayerRaw).strip().isdigit() and int(t2FocusPlayerRaw) > 0 else None
    if t1OffensiveFormation not in offensiveFormationDestinationWeights or t2OffensiveFormation not in offensiveFormationDestinationWeights:
        raise ValueError("Offensive formation must be Balanced, Motion, Pick-and-Roll, Post-Up, or Space-and-Post.")
    if t1DefensiveFormation not in defensiveFormationDestinationWeights or t2DefensiveFormation not in defensiveFormationDestinationWeights:
        raise ValueError("Defensive formation must be Man-to-Man, 1-3-1 Zone, 3-2 Zone, 2-3 Zone, or Box-and-One Zone.")
    t1FormationDestinationWeights = {zone:offensiveFormationDestinationWeights[t1OffensiveFormation][zone] * defensiveFormationDestinationWeights[t2DefensiveFormation][zone] for zone in ("inside","midrange","three")}
    t2FormationDestinationWeights = {zone:offensiveFormationDestinationWeights[t2OffensiveFormation][zone] * defensiveFormationDestinationWeights[t1DefensiveFormation][zone] for zone in ("inside","midrange","three")}
    t1FormationOffensiveReboundAdjustment = offensiveFormationReboundAdjustments[t1OffensiveFormation] + defensiveFormationOffensiveReboundAdjustments[t2DefensiveFormation]
    t2FormationOffensiveReboundAdjustment = offensiveFormationReboundAdjustments[t2OffensiveFormation] + defensiveFormationOffensiveReboundAdjustments[t1DefensiveFormation]
    paceActionTimeCategories = list(paceActionTimeModifiers.keys())
    t1ExpectedActionTimeModifier = sum(paceActionTimeModifiers[category] * weight for category,weight in zip(paceActionTimeCategories,paceActionTimeWeights[t1Pace])) / sum(paceActionTimeWeights[t1Pace])
    t2ExpectedActionTimeModifier = sum(paceActionTimeModifiers[category] * weight for category,weight in zip(paceActionTimeCategories,paceActionTimeWeights[t2Pace])) / sum(paceActionTimeWeights[t2Pace])
    t1roster_df["base_stamina"] = t1roster_df["stamina"].astype(float)
    t2roster_df["base_stamina"] = t2roster_df["stamina"].astype(float)
    t1roster_df["stamina"] = t1roster_df["base_stamina"] * t1PaceStaminaModifier
    t2roster_df["stamina"] = t2roster_df["base_stamina"] * t2PaceStaminaModifier

    t1teamstats = pd.DataFrame().assign(id=t1team_df['id'], Team=t1team_df['abbr'])
    t1teamstats['Assist'] = 0
    t1teamstats['Ins Shot Att'] = 0
    t1teamstats['Ins Shot Made'] = 0
    t1teamstats['Ins Shot %'] = 0
    t1teamstats['Mid Shot Att'] = 0
    t1teamstats['Mid Shot Made'] = 0
    t1teamstats['Mid Shot %'] = 0
    t1teamstats['3PT Shot Att'] = 0
    t1teamstats['3PT Shot Made'] = 0
    t1teamstats['3PT Shot %'] = 0
    t1teamstats['FT Shot Att'] = 0
    t1teamstats['FT Shot Made'] = 0
    t1teamstats['FT Shot %'] = 0
    t1teamstats['OREB'] = 0
    t1teamstats['DREB'] = 0
    t1teamstats['Stl'] = 0
    t1teamstats['Blk'] = 0
    t1teamstats['TO'] = 0
    t1teamstats['Foul'] = 0
    t1teamstats['Poss'] = 0
    t1teamstats['TOP'] = "00:00.0"
    t1teamstats['Pts'] = 0
    t1teamstats.set_index('id', inplace=True)

    t1teamscore = pd.DataFrame().assign(id=t1team_df['id'], Team=t1team_df['abbr'])
    t1teamscore['P1'] = 0
    t1teamscore['P2'] = 0
    t1teamscore['P3'] = 0
    t1teamscore['P4'] = 0
    t1teamscore['OT'] = 0
    t1teamscore.set_index('id', inplace=True)

    t2teamstats = pd.DataFrame().assign(id=t2team_df['id'], Team=t2team_df['abbr'])
    t2teamstats['Assist'] = 0
    t2teamstats['Ins Shot Att'] = 0
    t2teamstats['Ins Shot Made'] = 0
    t2teamstats['Ins Shot %'] = 0
    t2teamstats['Mid Shot Att'] = 0
    t2teamstats['Mid Shot Made'] = 0
    t2teamstats['Mid Shot %'] = 0
    t2teamstats['3PT Shot Att'] = 0
    t2teamstats['3PT Shot Made'] = 0
    t2teamstats['3PT Shot %'] = 0
    t2teamstats['FT Shot Att'] = 0
    t2teamstats['FT Shot Made'] = 0
    t2teamstats['FT Shot %'] = 0
    t2teamstats['OREB'] = 0
    t2teamstats['DREB'] = 0
    t2teamstats['Stl'] = 0
    t2teamstats['Blk'] = 0
    t2teamstats['TO'] = 0
    t2teamstats['Foul'] = 0
    t2teamstats['Poss'] = 0
    t2teamstats['TOP'] = "00:00.0"
    t2teamstats['Pts'] = 0
    t2teamstats.set_index('id', inplace=True)

    t2teamscore = pd.DataFrame().assign(id=t2team_df['id'], Team=t2team_df['abbr'])
    t2teamscore['P1'] = 0
    t2teamscore['P2'] = 0
    t2teamscore['P3'] = 0
    t2teamscore['P4'] = 0
    t2teamscore['OT'] = 0
    t2teamscore.set_index('id', inplace=True)

    t1StealProbability = stealProbability
    t1OtherTurnoverProbability = otherTurnoverProbability
    t1MoveAttemptProbability = moveAttemptProbability
    t1PassAttemptProbability = passAttemptProbability
    t1ShotAttemptProbability = shotAttemptProbability

    t2StealProbability = stealProbability
    t2OtherTurnoverProbability = otherTurnoverProbability
    t2MoveAttemptProbability = moveAttemptProbability
    t2PassAttemptProbability = passAttemptProbability
    t2ShotAttemptProbability = shotAttemptProbability

    t1Probabilities = {
        "steal": t1StealProbability,
        "other_turnover": t1OtherTurnoverProbability,
        "move": t1MoveAttemptProbability,
        "pass": t1PassAttemptProbability,
        "shot": t1ShotAttemptProbability,
    }

    t2Probabilities = {
        "steal": t2StealProbability,
        "other_turnover": t2OtherTurnoverProbability,
        "move": t2MoveAttemptProbability,
        "pass": t2PassAttemptProbability,
        "shot": t2ShotAttemptProbability,
    }

    t1Players, t2Players = getPlayers(t1Lineup_df,t2Lineup_df)

    t1FoulProtection = {"enabled":int(t1Gameplan_df["trigger1_enabled"].iloc[0] or 0),"type":int(t1Gameplan_df["trigger1_type"].iloc[0] or 0),"value":int(t1Gameplan_df["trigger1_value"].iloc[0] or 0)}
    t2FoulProtection = {"enabled":int(t2Gameplan_df["trigger1_enabled"].iloc[0] or 0),"type":int(t2Gameplan_df["trigger1_type"].iloc[0] or 0),"value":int(t2Gameplan_df["trigger1_value"].iloc[0] or 0)}
    t1TimeoutGameplan = {"preserve":int(t1Gameplan_df["preserve_timeouts"].iloc[0] or 0),"trigger2_enabled":int(t1Gameplan_df["trigger2_enabled"].iloc[0] or 0),"trigger2_value":int(t1Gameplan_df["trigger2_value"].iloc[0] or 0),"trigger3_enabled":int(t1Gameplan_df["trigger3_enabled"].iloc[0] or 0),"trigger3_value":int(t1Gameplan_df["trigger3_value"].iloc[0] or 0),"trigger3_exhaustion":int(t1Gameplan_df["trigger3_exhaustion"].iloc[0] or 0),"trigger4_enabled":int(t1Gameplan_df["trigger4_enabled"].iloc[0] or 0),"trigger4_value":int(t1Gameplan_df["trigger4_value"].iloc[0] or 0)}
    t2TimeoutGameplan = {"preserve":int(t2Gameplan_df["preserve_timeouts"].iloc[0] or 0),"trigger2_enabled":int(t2Gameplan_df["trigger2_enabled"].iloc[0] or 0),"trigger2_value":int(t2Gameplan_df["trigger2_value"].iloc[0] or 0),"trigger3_enabled":int(t2Gameplan_df["trigger3_enabled"].iloc[0] or 0),"trigger3_value":int(t2Gameplan_df["trigger3_value"].iloc[0] or 0),"trigger3_exhaustion":int(t2Gameplan_df["trigger3_exhaustion"].iloc[0] or 0),"trigger4_enabled":int(t2Gameplan_df["trigger4_enabled"].iloc[0] or 0),"trigger4_value":int(t2Gameplan_df["trigger4_value"].iloc[0] or 0)}

    t1RosterById = indexRoster(t1roster_df)
    t2RosterById = indexRoster(t2roster_df)

    t1RecoveryMinutes = {int(playerId): 0.0 for playerId in t1RosterById.index}
    t2RecoveryMinutes = {int(playerId): 0.0 for playerId in t2RosterById.index}
    t1FoulProtectionBench = set()
    t2FoulProtectionBench = set()
    t1PlayerHalfFouls = {}
    t2PlayerHalfFouls = {}
    momentum = 0.0
    teamTimeoutsRemaining = {t1:(4 if league == "CBB" else 7),t2:(4 if league == "CBB" else 7)}
    teamTimeoutTriggerLatches = {t1:{"trigger2":False,"trigger3":False,"trigger4":False},t2:{"trigger2":False,"trigger3":False,"trigger4":False}}
    teamTimeoutPreservationAnnounced = {t1:False,t2:False}
    teamTimeoutBlockedUntilLiveAction = False

    t1onCourt = []
    t2onCourt = []

    def getActiveLineupPreferences(onCourt):
        if not onCourt:
            return {"inside":lineupPreferenceNeutralShare,"midrange":lineupPreferenceNeutralShare,"three":lineupPreferenceNeutralShare}
        return {"inside":sum(float(player["inside_preference"]) for player in onCourt.values()) / len(onCourt),"midrange":sum(float(player["midrange_preference"]) for player in onCourt.values()) / len(onCourt),"three":sum(float(player["three_preference"]) for player in onCourt.values()) / len(onCourt)}

    def getActiveDestinationWeights(onCourt,formationDestinationWeights):
        lineupPreferences = getActiveLineupPreferences(onCourt)
        preferenceWeights = {}
        for zone in ("inside","midrange","three"):
            preferenceWeight = (lineupPreferences[zone] / lineupPreferenceNeutralShare) ** lineupPreferenceDestinationStrength if lineupPreferences[zone] > 0 else lineupPreferenceDestinationMinimum
            preferenceWeights[zone] = max(lineupPreferenceDestinationMinimum,min(lineupPreferenceDestinationMaximum,preferenceWeight))
        return {zone:formationDestinationWeights[zone] * preferenceWeights[zone] for zone in ("inside","midrange","three")},lineupPreferences

    def getPreferenceZone(shotZone):
        if shotZone in ("inside","paint"):
            return "inside"
        if shotZone == "midrange":
            return "midrange"
        if shotZone in ("three","corner_three"):
            return "three"
        return None

    def foulProtectionActive():
        if period > periodPerGame:
            return False
        if period == periodPerGame and currTime <= 120:
            return False
        return True

    def registerFoulProtection(teamNumber,playerStatId,playerId,playerLabel):
        if teamNumber == 1:
            protection = t1FoulProtection
            halfFouls = t1PlayerHalfFouls
            protectionBench = t1FoulProtectionBench
        else:
            protection = t2FoulProtection
            halfFouls = t2PlayerHalfFouls
            protectionBench = t2FoulProtectionBench

        if league == "CBB":
            halfNumber = 1 if period == 1 else 2
        else:
            halfNumber = 1 if period <= 2 else 2

        foulKey = (halfNumber,int(playerId))
        halfFouls[foulKey] = halfFouls.get(foulKey,0) + 1

        if not foulProtectionActive() or protection["enabled"] != 1:
            return False

        if protection["type"] == 1:
            threshold = 2
            playerProtected = int(playerStatId) == protection["value"]
        elif protection["type"] == 2:
            threshold = protection["value"]
            playerProtected = threshold >= 1
        else:
            return False

        if not playerProtected or halfFouls[foulKey] < threshold or int(playerId) in protectionBench:
            return False

        protectionBench.add(int(playerId))
        print(f"Foul Protection: {playerLabel} has {halfFouls[foulKey]} fouls in this half and will remain on the bench until the next half.")
        return True

    def pullSubs(starters,protectedPlayer=None):
        t1ProtectedPlayerId = None
        t1ProtectedSlot = None
        t1ProtectedSourceSlot = None
        t2ProtectedPlayerId = None
        t2ProtectedSlot = None
        t2ProtectedSourceSlot = None

        if protectedPlayer is not None:
            protectedPlayerId = int(protectedPlayer["player_id"])
            t1ProtectedSlot = getOnCourtSlot(protectedPlayer,t1onCourt)
            t2ProtectedSlot = getOnCourtSlot(protectedPlayer,t2onCourt)

            if t1ProtectedSlot is not None:
                t1ProtectedPlayerId = protectedPlayerId
                t1ProtectedSourceSlot = protectedPlayer.get("lineup_source_slot")
                t2ProtectedSlot = None
            elif t2ProtectedSlot is not None:
                t2ProtectedPlayerId = protectedPlayerId
                t2ProtectedSourceSlot = protectedPlayer.get("lineup_source_slot")
                t1ProtectedSlot = None
            else:
                raise ValueError(f"Protected player ID {protectedPlayerId} is not currently on the court.")

        t1ExcludedPlayerIds = set(t1FouledOutPlayerIds)
        t2ExcludedPlayerIds = set(t2FouledOutPlayerIds)
        if foulProtectionActive():
            t1ExcludedPlayerIds.update(t1FoulProtectionBench)
            t2ExcludedPlayerIds.update(t2FoulProtectionBench)

        newT1OnCourt,newT2OnCourt,newLineupParameters = setLineups(
            t1Players=t1Players,
            t2Players=t2Players,
            t1RosterById=t1RosterById,
            t2RosterById=t2RosterById,
            t1Probabilities=t1Probabilities,
            t2Probabilities=t2Probabilities,
            HCAAdj=HCAAdj,
            forceStarters=starters,
            t1ExcludedPlayerIds=t1ExcludedPlayerIds,
            t2ExcludedPlayerIds=t2ExcludedPlayerIds,
            t1ProtectedPlayerId=t1ProtectedPlayerId,
            t1ProtectedSlot=t1ProtectedSlot,
            t2ProtectedPlayerId=t2ProtectedPlayerId,
            t2ProtectedSlot=t2ProtectedSlot,
            t1ProtectedSourceSlot=t1ProtectedSourceSlot,
            t2ProtectedSourceSlot=t2ProtectedSourceSlot,
        )
        newLineupParameters["t1OffensiveRebound"] = max(0.0,min(1.0,newLineupParameters["t1OffensiveRebound"] + t1FormationOffensiveReboundAdjustment))
        newLineupParameters["t2OffensiveRebound"] = max(0.0,min(1.0,newLineupParameters["t2OffensiveRebound"] + t2FormationOffensiveReboundAdjustment))
        return newT1OnCourt,newT2OnCourt,newLineupParameters

    def pullFreeThrowSubs(protectedPlayer):
        nonlocal t1onCourt,t2onCourt,lineupParameters
        t1onCourt,t2onCourt,lineupParameters = pullSubs(False,protectedPlayer)
        print(t1 + " Free Throw Subs:")
        for lineupPlayer in t1onCourt.values():
            print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])
        print(t2 + " Free Throw Subs:")
        for lineupPlayer in t2onCourt.values():
            print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])

    def adjustMomentum(momentumTeam,momentumAmount,momentumReason):
        nonlocal momentum
        oldMomentum = momentum
        momentumDirection = -1.0 if momentumTeam == t1 else 1.0
        momentum = max(-1.0,min(1.0,momentum + (momentumDirection * float(momentumAmount))))
        print(f"Momentum event: {momentumReason} | {oldMomentum:+.2f} -> {momentum:+.2f}")

    def dampenMomentum(momentumRetention,momentumReason):
        nonlocal momentum
        oldMomentum = momentum
        momentum = max(-1.0,min(1.0,momentum * float(momentumRetention)))
        print(f"Momentum slowdown: {momentumReason} | {oldMomentum:+.2f} -> {momentum:+.2f}")

    def printMomentumMeter():
        momentumPosition = max(0,min(10,int(round((momentum + 1.0) * 5.0))))
        momentumSlots = ["-"] * 11
        momentumSlots[momentumPosition] = "x"
        if momentum < 0:
            momentumTeam = t1
            momentumStrength = abs(momentum)
        elif momentum > 0:
            momentumTeam = t2
            momentumStrength = momentum
        else:
            momentumTeam = "Neutral"
            momentumStrength = 0.0
        print(t1 + " |" + "".join(momentumSlots) + "| "+ t2 + f"  Momentum: {momentumTeam} {momentumStrength:.0%}")

    def getMomentumAdjustedRating(staminaAdjustedRating,ratingTeam):
        if ratingTeam == t1:
            momentumStrength = max(0.0,-momentum)
        elif ratingTeam == t2:
            momentumStrength = max(0.0,momentum)
        else:
            momentumStrength = 0.0
        momentumBonus = momentumStrength * momentumMaximumAttributeBonus
        momentumModifier = 1.0 + momentumBonus
        momentumAdjustedRating = float(staminaAdjustedRating) * momentumModifier
        return momentumAdjustedRating,momentumStrength,momentumBonus,momentumModifier

    def addPlayingTime(elapsedTime):
        elapsedTime = round(float(elapsedTime), 2)
        if elapsedTime <= 0:
            return
        for player in t1onCourt.values():
            playerId = player["id"].item()
            t1stats.at[playerId, "MP"] += elapsedTime
        for player in t2onCourt.values():
            playerId = player["id"].item()
            t2stats.at[playerId, "MP"] += elapsedTime

    def applyFatigueRecovery(recoveryAmount,recoveryLabel):
        recoveryAmount = max(0.0,float(recoveryAmount))

        for playerId in t1RecoveryMinutes:
            statId = t1RosterById.at[playerId,"id"]
            minutesPlayed = float(t1stats.at[statId,"MP"]) / 60
            t1RecoveryMinutes[playerId] = min(minutesPlayed,t1RecoveryMinutes[playerId] + recoveryAmount)

        for playerId in t2RecoveryMinutes:
            statId = t2RosterById.at[playerId,"id"]
            minutesPlayed = float(t2stats.at[statId,"MP"]) / 60
            t2RecoveryMinutes[playerId] = min(minutesPlayed,t2RecoveryMinutes[playerId] + recoveryAmount)

        print(f"{recoveryLabel}: all players receive up to {recoveryAmount:.2f} minutes of fatigue recovery.")

    def completeMediaTimeout(mediaTimeoutLabel,protectedPlayer=None):
        nonlocal t1onCourt,t2onCourt,lineupParameters,teamTimeoutBlockedUntilLiveAction
        print(f"{mediaTimeoutLabel} at {int(currTime // 60):02d}:{currTime % 60:04.1f}.")
        applyFatigueRecovery(mediaTimeoutRecoveryMinutes,"Media-timeout breather")
        dampenMomentum(momentumMediaTimeoutRetention,"media timeout")
        t1onCourt,t2onCourt,lineupParameters = pullSubs(False,protectedPlayer)
        teamTimeoutBlockedUntilLiveAction = True
        print(t1 + " Media Timeout Subs:")
        for i in list(t1onCourt.values()):
            print(i["position"] + " " + i["first_name"] + " " + i["last_name"])
        print(t2 + " Media Timeout Subs:")
        for i in list(t2onCourt.values()):
            print(i["position"] + " " + i["first_name"] + " " + i["last_name"])

    def convertTeamTimeoutToMediaTimeout(protectedPlayer=None):
        if period > periodPerGame:
            return False
        if league == "CBB":
            for mediaTimeoutMark in cbbMediaTimeoutMarks:
                if mediaTimeoutMark not in cbbMediaTimeoutsTaken[period] and mediaTimeoutMark <= currTime <= mediaTimeoutMark + 30:
                    cbbMediaTimeoutsTaken[period].add(mediaTimeoutMark)
                    completeMediaTimeout(f"Under-{int(mediaTimeoutMark / 60)} media timeout converted from a team timeout",protectedPlayer)
                    return True
        else:
            if nbaTimeoutEventsByPeriod[period] == 0 and 420 <= currTime <= 450:
                nbaTimeoutEventsByPeriod[period] = 1
                completeMediaTimeout("Under-7 mandatory media timeout converted from a team timeout",protectedPlayer)
                return True
            if nbaTimeoutEventsByPeriod[period] == 1 and 180 <= currTime <= 210:
                nbaTimeoutEventsByPeriod[period] = 2
                completeMediaTimeout("Under-3 mandatory media timeout converted from a team timeout",protectedPlayer)
                return True
        return False

    def checkMediaTimeout(protectedPlayer=None):
        nonlocal t1onCourt, t2onCourt, lineupParameters
        if period > periodPerGame:
            return False

        mediaTimeoutLabel = None

        if league == "CBB":
            for mediaTimeoutMark in cbbMediaTimeoutMarks:
                if currTime < mediaTimeoutMark and mediaTimeoutMark not in cbbMediaTimeoutsTaken[period]:
                    cbbMediaTimeoutsTaken[period].add(mediaTimeoutMark)
                    mediaTimeoutLabel = f"Under-{int(mediaTimeoutMark / 60)} media timeout"
                    break
        else:
            if currTime < 420 and nbaTimeoutEventsByPeriod[period] == 0:
                nbaTimeoutEventsByPeriod[period] += 1
                mediaTimeoutLabel = "Under-7 mandatory media timeout"
            elif currTime < 180 and nbaTimeoutEventsByPeriod[period] == 1:
                nbaTimeoutEventsByPeriod[period] += 1
                mediaTimeoutLabel = "Under-3 mandatory media timeout"

        if mediaTimeoutLabel is None:
            return False

        completeMediaTimeout(mediaTimeoutLabel,protectedPlayer)
        return True

    def getPlayerExhaustionPercent(player,team):
        playerStatId = int(player["id"])
        playerMinutes = float((t1stats if team == t1 else t2stats).at[playerStatId,"MP"]) / 60
        playerRecoveryMinutes = getPlayerRecoveryMinutes(player)
        staminaCapacity = max(1.0,float(player["stamina"]))
        return max(0.0,(playerMinutes - playerRecoveryMinutes) / staminaCapacity * 100)

    def getTeamTimeoutConditions(timeoutTeam):
        gameplan = t1TimeoutGameplan if timeoutTeam == t1 else t2TimeoutGameplan
        onCourt = t1onCourt if timeoutTeam == t1 else t2onCourt
        opponentPoints = t2pts if timeoutTeam == t1 else t1pts
        teamPoints = t1pts if timeoutTeam == t1 else t2pts
        opponentLead = opponentPoints - teamPoints
        trigger2Active = gameplan["trigger2_enabled"] == 1 and opponentLead >= gameplan["trigger2_value"]
        monitoredPlayer = next((player for player in onCourt.values() if int(player["id"]) == gameplan["trigger3_value"]),None)
        monitoredExhaustion = getPlayerExhaustionPercent(monitoredPlayer,timeoutTeam) if monitoredPlayer is not None else 0.0
        trigger3Active = gameplan["trigger3_enabled"] == 1 and monitoredPlayer is not None and monitoredExhaustion >= gameplan["trigger3_exhaustion"]
        playerExhaustionValues = [getPlayerExhaustionPercent(player,timeoutTeam) for player in onCourt.values()]
        averageExhaustion = sum(playerExhaustionValues) / len(playerExhaustionValues) if playerExhaustionValues else 0.0
        trigger4Active = gameplan["trigger4_enabled"] == 1 and averageExhaustion >= gameplan["trigger4_value"]
        conditions = {"trigger2":trigger2Active,"trigger3":trigger3Active,"trigger4":trigger4Active}
        details = {"trigger2":f"opponent lead {opponentLead} points (threshold {gameplan['trigger2_value']})","trigger3":f"designated player exhaustion {monitoredExhaustion:.1f}% (threshold {gameplan['trigger3_exhaustion']}%)","trigger4":f"on-court average exhaustion {averageExhaustion:.1f}% (threshold {gameplan['trigger4_value']}%)"}
        return conditions,details

    def checkTeamTimeout(priorityTeam,allowNonPossession=False,protectedPlayer=None):
        nonlocal t1onCourt,t2onCourt,lineupParameters,teamTimeoutBlockedUntilLiveAction
        if priorityTeam not in (t1,t2):
            return False
        if teamTimeoutBlockedUntilLiveAction:
            teamTimeoutBlockedUntilLiveAction = False
            return False
        timeoutCandidates = [priorityTeam]
        if allowNonPossession:
            timeoutCandidates.append(t2 if priorityTeam == t1 else t1)
        for timeoutTeam in timeoutCandidates:
            conditions,details = getTeamTimeoutConditions(timeoutTeam)
            for triggerName,conditionActive in conditions.items():
                if not conditionActive:
                    teamTimeoutTriggerLatches[timeoutTeam][triggerName] = False
            timeoutReasons = [details[triggerName] for triggerName,conditionActive in conditions.items() if conditionActive and not teamTimeoutTriggerLatches[timeoutTeam][triggerName]]
            if teamTimeoutsRemaining[timeoutTeam] <= 0 or not timeoutReasons:
                continue
            timeoutGameplan = t1TimeoutGameplan if timeoutTeam == t1 else t2TimeoutGameplan
            preserveFinalTimeout = timeoutGameplan["preserve"] == 1 and teamTimeoutsRemaining[timeoutTeam] == 1 and not (period > periodPerGame or (period == periodPerGame and currTime <= 120))
            if preserveFinalTimeout:
                if not teamTimeoutPreservationAnnounced[timeoutTeam]:
                    print(f"{timeoutTeam} preserves its final timeout for the last two minutes. Automatic timeout triggers are temporarily blocked.")
                    teamTimeoutPreservationAnnounced[timeoutTeam] = True
                continue
            if teamTimeoutPreservationAnnounced[timeoutTeam]:
                print(f"{timeoutTeam} timeout preservation restriction has been removed.")
                teamTimeoutPreservationAnnounced[timeoutTeam] = False
            for triggerName,conditionActive in conditions.items():
                if conditionActive:
                    teamTimeoutTriggerLatches[timeoutTeam][triggerName] = True
            print(f"{timeoutTeam} requests a timeout: " + "; ".join(timeoutReasons) + ".")
            if convertTeamTimeoutToMediaTimeout(protectedPlayer):
                print(f"The timeout is charged as a media timeout. {timeoutTeam} keeps all {teamTimeoutsRemaining[timeoutTeam]} team timeouts.")
                return True
            teamTimeoutsRemaining[timeoutTeam] -= 1
            print(f"{timeoutTeam} TEAM TIMEOUT at {int(currTime // 60):02d}:{currTime % 60:04.1f}. Timeouts remaining: {teamTimeoutsRemaining[timeoutTeam]}.")
            applyFatigueRecovery(teamTimeoutRecoveryMinutes,f"{timeoutTeam} team-timeout breather")
            dampenMomentum(momentumTeamTimeoutRetention,f"{timeoutTeam} team timeout")
            t1onCourt,t2onCourt,lineupParameters = pullSubs(False,protectedPlayer)
            teamTimeoutBlockedUntilLiveAction = True
            if league != "CBB" and period <= periodPerGame:
                nbaTimeoutEventsByPeriod[period] = 2
            print(t1 + " Team Timeout Subs:")
            for lineupPlayer in t1onCourt.values():
                print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])
            print(t2 + " Team Timeout Subs:")
            for lineupPlayer in t2onCourt.values():
                print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])
            return True
        return False

    def checkTimeoutStoppage(priorityTeam,allowNonPossession=False,protectedPlayer=None):
        if checkMediaTimeout(protectedPlayer):
            return True
        return checkTeamTimeout(priorityTeam,allowNonPossession,protectedPlayer)

    def getPlayerRecoveryMinutes(player):
        playerId = int(player["player_id"])
        if playerId in t1RecoveryMinutes:
            return t1RecoveryMinutes[playerId]
        if playerId in t2RecoveryMinutes:
            return t2RecoveryMinutes[playerId]
        return 0.0

    t1onCourt, t2onCourt, lineupParameters = pullSubs(True)

    t1TipChance = ((t1onCourt["c1"]["height"] - t2onCourt["c1"]["height"]) * 0.1) + 0.5
    t2TipChance = 1 - t1TipChance

    possTeam = "TIPOFF"
    possPlayer = ""
    assistPlayer = None
    assistMovementCount = 0
    defendedPlayerId = None
    currentDefender = None
    previousDefender = None
    finalHeavePending = False
    teamPossessions = {t1:0,t2:0}
    teamPossessionTime = {t1:0.0,t2:0.0}
    lastCountedPossessionTeam = None

    while gameOn and periodOn:
        tipoffJustOccurred = False

        if courtPos == (-4, 1):
            footerPos = "|x        |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-3, 1):
            footerPos = "|  x      |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-2, 1):
            footerPos = "|    x    |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-1, 1):
            footerPos = "|      x  |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (0, 1):
            footerPos = "|         x         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (1, 1):
            footerPos = "|         |  x      |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (2, 1):
            footerPos = "|         |    x    |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (3, 1):
            footerPos = "|         |      x  |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (4, 1):
            footerPos = "|         |        x|\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-4, 2):
            footerPos = "|         |         |\n|x        |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-3, 2):
            footerPos = "|         |         |\n|  x      |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-2, 2):
            footerPos = "|         |         |\n|    x    |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-1, 2):
            footerPos = "|         |         |\n|      x  |         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (0, 2):
            footerPos = "|         |         |\n|         x         |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (1, 2):
            footerPos = "|         |         |\n|         |  x      |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (2, 2):
            footerPos = "|         |         |\n|         |    x    |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (3, 2):
            footerPos = "|         |         |\n|         |      x  |\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (4, 2):
            footerPos = "|         |         |\n|         |        x|\n|-O       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-4, 3):
            footerPos = "|         |         |\n|         |         |\n|-x       |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-3, 3):
            footerPos = "|         |         |\n|         |         |\n|-Ox      |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-2, 3):
            footerPos = "|         |         |\n|         |         |\n|-O  x    |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (-1, 3):
            footerPos = "|         |         |\n|         |         |\n|-O    x  |       O-|\n|         |         |\n|         |         |"
        elif courtPos == (0, 3):
            footerPos = "|         |         |\n|         |         |\n|-O       x       O-|\n|         |         |\n|         |         |"
        elif courtPos == (1, 3):
            footerPos = "|         |         |\n|         |         |\n|-O       |  x    O-|\n|         |         |\n|         |         |"
        elif courtPos == (2, 3):
            footerPos = "|         |         |\n|         |         |\n|-O       |    x  O-|\n|         |         |\n|         |         |"
        elif courtPos == (3, 3):
            footerPos = "|         |         |\n|         |         |\n|-O       |      xO-|\n|         |         |\n|         |         |"
        elif courtPos == (4, 3):
            footerPos = "|         |         |\n|         |         |\n|-O       |       x-|\n|         |         |\n|         |         |"
        elif courtPos == (-4, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|x        |         |\n|         |         |"
        elif courtPos == (-3, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|  x      |         |\n|         |         |"
        elif courtPos == (-2, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|    x    |         |\n|         |         |"
        elif courtPos == (-1, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|      x  |         |\n|         |         |"
        elif courtPos == (0, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         x         |\n|         |         |"
        elif courtPos == (1, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |  x      |\n|         |         |"
        elif courtPos == (2, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |    x    |\n|         |         |"
        elif courtPos == (3, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |      x  |\n|         |         |"
        elif courtPos == (4, 4):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |        x|\n|         |         |"
        elif courtPos == (-4, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|x        |         |"
        elif courtPos == (-3, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|  x      |         |"
        elif courtPos == (-2, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|    x    |         |"
        elif courtPos == (-1, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|      x  |         |"
        elif courtPos == (0, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         x         |"
        elif courtPos == (1, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |  x      |"
        elif courtPos == (2, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |    x    |"
        elif courtPos == (3, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |      x  |"
        elif courtPos == (4, 5):
            footerPos = "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |        x|"
        else:
            footerPos = "TIPOFF"

        displayGameTime = max(0, math.ceil(currTime))
        displayShotClock = max(0, math.ceil(currShotClock))

        qtrminutes, qtrseconds = divmod(displayGameTime, 60)
        qtrhours, qtrminutes = divmod(qtrminutes, 60)

        shotminutes, shotseconds = divmod(displayShotClock, 60)
        shothours, shotminutes = divmod(shotminutes, 60)

        if possTeam == "TIPOFF":
            print("Game Starting\nT1 (Home): " + t1 + "\nT2 (Away): " + t2)
            print(f"{t1} Pace: {t1Pace} | Available stamina modifier: {t1PaceStaminaModifier:.0%} | Expected action-time modifier: {t1ExpectedActionTimeModifier:.2f}")
            print(f"{t2} Pace: {t2Pace} | Available stamina modifier: {t2PaceStaminaModifier:.0%} | Expected action-time modifier: {t2ExpectedActionTimeModifier:.2f}")
            print(f"{t1} Formations: {t1OffensiveFormation} offense vs {t2DefensiveFormation} defense | Destination weights: inside {t1FormationDestinationWeights['inside']:.3f}, midrange {t1FormationDestinationWeights['midrange']:.3f}, three {t1FormationDestinationWeights['three']:.3f} | OREB adjustment: {t1FormationOffensiveReboundAdjustment:+.2%} | Opponent focus: {t2FocusPlayerId or 'none'}")
            print(f"{t2} Formations: {t2OffensiveFormation} offense vs {t1DefensiveFormation} defense | Destination weights: inside {t2FormationDestinationWeights['inside']:.3f}, midrange {t2FormationDestinationWeights['midrange']:.3f}, three {t2FormationDestinationWeights['three']:.3f} | OREB adjustment: {t2FormationOffensiveReboundAdjustment:+.2%} | Opponent focus: {t1FocusPlayerId or 'none'}")
            print(t1 + " Starters:")
            for i in list(t1onCourt.values()):
                print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
            print(t2 + " Starters:")
            for i in list(t2onCourt.values()):
                print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
            tipOff = random.random()
            if tipOff < t1TipChance:
                tippedTo = random.choice(list(t1onCourt.values()))
                possPlayer = tippedTo
                possTeam = t1
                offense = t1
                defense = t2
                offense_df = t1onCourt
                defense_df = t2onCourt
                addPlayingTime(1)
                currTime -= 1
                print(str(t1onCourt["c1"]["position"]) + " " + str(t1onCourt["c1"]["first_name"])+ " " + str(t1onCourt["c1"]["last_name"]) + " wins the tipoff for " + t1 + ". " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes control of the ball.")
                #print("Game Clock: " +game_clock_text + " / Shot Clock: "  + ":%02d" % (shotseconds))
                tipoffJustOccurred = True
            else:
                tippedTo = random.choice(list(t2onCourt.values()))
                possPlayer = tippedTo
                possTeam = t2
                offense = t2
                defense = t1
                offense_df = t2onCourt
                defense_df = t1onCourt
                addPlayingTime(1)
                currTime -= 1
                print(str(t2onCourt["c1"]["position"]) + " " + str(t2onCourt["c1"]["first_name"])+ " " + str(t2onCourt["c1"]["last_name"]) + " wins the tipoff for " + t2 + ". " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes control of the ball.")
                #print("Game Clock: " +game_clock_text + " / Shot Clock: "  + "%02d" % (shotseconds))
                tipoffJustOccurred = True

        if possTeam == "OT_TIPOFF":
            tipOff = random.random()
            if tipOff < t1TipChance:
                tippedTo = random.choice(list(t1onCourt.values()))
                possPlayer = tippedTo
                possTeam = t1
                offense = t1
                defense = t2
                offense_df = t1onCourt
                defense_df = t2onCourt
                addPlayingTime(1)
                currTime -= 1
                print(str(t1onCourt["c1"]["position"]) + " " + str(t1onCourt["c1"]["first_name"])+ " " + str(t1onCourt["c1"]["last_name"]) + " wins the tipoff for " + t1 + ". " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes control of the ball.")
                #print("Game Clock: " +game_clock_text + " / Shot Clock: "  + ":%02d" % (shotseconds))
                tipoffJustOccurred = True
            else:
                tippedTo = random.choice(list(t2onCourt.values()))
                possPlayer = tippedTo
                possTeam = t2
                offense = t2
                defense = t1
                offense_df = t2onCourt
                defense_df = t1onCourt
                addPlayingTime(1)
                currTime -= 1
                print(str(t2onCourt["c1"]["position"]) + " " + str(t2onCourt["c1"]["first_name"])+ " " + str(t2onCourt["c1"]["last_name"]) + " wins the tipoff for " + t2 + ". " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes control of the ball.")
                #print("Game Clock: " +game_clock_text + " / Shot Clock: "  + "%02d" % (shotseconds))
                tipoffJustOccurred = True

        if possTeam == t1 or possTeam == t2:
            if possTeam != lastCountedPossessionTeam:
                teamPossessions[possTeam] += 1
                lastCountedPossessionTeam = possTeam
            if tipoffJustOccurred:
                teamPossessionTime[possTeam] += 1.0

            if possTeam == t1:
                offense = t1
                defense = t2
                offense_df = t1onCourt
                defense_df = t2onCourt
                team_side = "HOME"

                actionParameters = {
                    "steal_cutoff": lineupParameters["t1StealCutoff"],
                    "turnover_cutoff": lineupParameters["t1TOCutoff"],
                    "move_cutoff": lineupParameters["t1MoveCutoff"],
                    "pass_cutoff": lineupParameters["t1PassCutoff"],
                    "shot_cutoff": lineupParameters["t1ShotCutoff"],
                }

            elif possTeam == t2:
                offense = t2
                defense = t1
                offense_df = t2onCourt
                defense_df = t1onCourt
                team_side = "AWAY"

                actionParameters = {
                    "steal_cutoff": lineupParameters["t2StealCutoff"],
                    "turnover_cutoff": lineupParameters["t2TOCutoff"],
                    "move_cutoff": lineupParameters["t2MoveCutoff"],
                    "pass_cutoff": lineupParameters["t2PassCutoff"],
                    "shot_cutoff": lineupParameters["t2ShotCutoff"],
                }

            if not tipoffJustOccurred and checkTeamTimeout(possTeam,False,possPlayer):
                defendedPlayerId = None
                currentDefender = None
                previousDefender = None
                continue

            attemptFinalHeave = False
            finalHeaveStartedAfterInbound = finalHeavePending
            finalHeavePending = False

            if possTeam == t1:
                finalHeaveScoringDeficit = t2pts - t1pts
            else:
                finalHeaveScoringDeficit = t1pts - t2pts

            if not tipoffJustOccurred and period >= periodPerGame and 0 < currTime <= finalHeaveMaximumTime and 0 <= finalHeaveScoringDeficit <= 3:
                if finalHeaveStartedAfterInbound:
                    finalHeaveInbounder = possPlayer
                    finalHeaveShooters = [player for player in offense_df.values() if int(player["player_id"]) != int(finalHeaveInbounder["player_id"])]

                    if finalHeaveShooters:
                        finalHeaveShooterWeights = [max(0.01,float(player["shooting3"]) * float(player["bbiq"])) for player in finalHeaveShooters]
                        possPlayer = random.choices(finalHeaveShooters,weights=finalHeaveShooterWeights,k=1)[0]

                    print(f"With {currTime:.1f} seconds remaining, {finalHeaveInbounder['position']} {finalHeaveInbounder['first_name']} {finalHeaveInbounder['last_name']} inbounds to {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} for a final heave.")
                else:
                    print(f"With {currTime:.1f} seconds remaining, {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} recognizes the clock and prepares a final heave.")

                attemptFinalHeave = True

            possPlayerId = int(
                possPlayer["id"]
            )

            if defendedPlayerId != possPlayerId:
                previousDefender = currentDefender

                if possTeam == t1:
                    currentDefender = selectDefender(
                        possPlayer,
                        t1onCourt,
                        t2onCourt,
                        excluded_defender=previousDefender
                    )
                else:
                    currentDefender = selectDefender(
                        possPlayer,
                        t2onCourt,
                        t1onCourt,
                        excluded_defender=previousDefender
                    )

                defendedPlayerId = possPlayerId

            defender = currentDefender

            offense_slot = getOnCourtSlot(
                possPlayer,
                offense_df
            )

            defense_slot = getOnCourtSlot(
                defender,
                defense_df
            )

            print(
                f"Matchup: "
                f"{possPlayer['position']} "
                f"{possPlayer['first_name']} "
                f"{possPlayer['last_name']} "
                f"({offense_slot}) vs "
                f"{defender['position']} "
                f"{defender['first_name']} "
                f"{defender['last_name']} "
                f"({defense_slot})"
            )

            baseStealProbability = actionParameters["steal_cutoff"]
            baseTurnoverProbability = actionParameters["turnover_cutoff"] - actionParameters["steal_cutoff"]
            baseMoveProbability = actionParameters["move_cutoff"] - actionParameters["turnover_cutoff"]
            basePassProbability = actionParameters["pass_cutoff"] - actionParameters["move_cutoff"]
            baseShotProbability = max(0.0,1.0 - actionParameters["pass_cutoff"])

            offensePace = t1Pace if offense == t1 else t2Pace
            activeDefensiveFormation = t2DefensiveFormation if offense == t1 else t1DefensiveFormation
            defensiveFocusPlayerId = t2FocusPlayerId if offense == t1 else t1FocusPlayerId
            focusPlayerOnCourt = defensiveFocusPlayerId is not None and any(int(player["id"]) == defensiveFocusPlayerId for player in offense_df.values())
            if activeDefensiveFormation in doubleTeamAdjustments and focusPlayerOnCourt:
                doubleTeamRole = "focus" if int(possPlayer["id"]) == defensiveFocusPlayerId else "teammate"
                doubleTeamShotAdjustment = doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole]["shot"]
                doubleTeamMovementAdjustment = doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole]["movement"]
                doubleTeamPassDeflectionAdjustment = doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole]["pass_deflection"]
            else:
                doubleTeamRole = "inactive"
                doubleTeamShotAdjustment = 0.0
                doubleTeamMovementAdjustment = 0.0
                doubleTeamPassDeflectionAdjustment = 0.0
            offenseShotClockUrgencyStart = paceShotClockUrgencyStarts[league][offensePace]
            shotClockUrgencyProgress = max(0.0,min(1.0,(offenseShotClockUrgencyStart - currShotClock) / offenseShotClockUrgencyStart))
            shotClockBBIQ = float(possPlayer["bbiq"])
            shotClockBBIQDifference = shotClockBBIQ - shotClockAwarenessAverageBBIQ
            shotClockEffectiveBBIQDifference = max(-shotClockAwarenessMaximumBBIQGap,min(shotClockAwarenessMaximumBBIQGap,shotClockBBIQDifference))
            shotClockAwarenessModifier = 1.0 + (shotClockEffectiveBBIQDifference * shotClockAwarenessModifierPerPoint)
            requestedShotClockUrgencyBonus = shotClockUrgencyMaximumBonus * (shotClockUrgencyProgress ** 2) * shotClockAwarenessModifier

            availableMovePassProbability = max(0.0,baseMoveProbability + basePassProbability)
            maximumShotClockTransfer = max(0.0,shotClockUrgencyMaximumShotProbability - baseShotProbability)
            shotClockUrgencyTransfer = min(requestedShotClockUrgencyBonus,maximumShotClockTransfer,availableMovePassProbability)

            if availableMovePassProbability > 0:
                remainingMovePassScale = (availableMovePassProbability - shotClockUrgencyTransfer) / availableMovePassProbability
            else:
                remainingMovePassScale = 0.0

            adjustedMoveProbability = baseMoveProbability * remainingMovePassScale
            adjustedPassProbability = basePassProbability * remainingMovePassScale
            adjustedShotProbability = baseShotProbability + shotClockUrgencyTransfer

            zone = get_shot_zone(courtPos)
            preferenceZone = getPreferenceZone(zone)
            activeLineupPreferences = getActiveLineupPreferences(offense_df)
            playerShotPreference = None
            playerShotWillingnessAdjustment = 0.0
            playerShotWillingnessTransfer = 0.0
            if preferenceZone is not None and is_in_frontcourt(team_side,courtPos):
                preferenceColumn = {"inside":"inside_preference","midrange":"midrange_preference","three":"three_preference"}[preferenceZone]
                playerShotPreference = float(possPlayer[preferenceColumn])
                playerShotWillingnessAdjustment = max(-playerShotWillingnessMaximumAdjustment,min(playerShotWillingnessMaximumAdjustment,(playerShotPreference - activeLineupPreferences[preferenceZone]) * playerShotWillingnessPerProportionPoint))
                availableAdjustedMovePassProbability = adjustedMoveProbability + adjustedPassProbability
                if playerShotWillingnessAdjustment > 0:
                    playerShotWillingnessTransfer = min(playerShotWillingnessAdjustment,availableAdjustedMovePassProbability,shotClockUrgencyMaximumShotProbability - adjustedShotProbability)
                    if availableAdjustedMovePassProbability > 0:
                        willingnessMovePassScale = (availableAdjustedMovePassProbability - playerShotWillingnessTransfer) / availableAdjustedMovePassProbability
                        adjustedMoveProbability *= willingnessMovePassScale
                        adjustedPassProbability *= willingnessMovePassScale
                    adjustedShotProbability += playerShotWillingnessTransfer
                elif playerShotWillingnessAdjustment < 0:
                    playerShotWillingnessTransfer = min(-playerShotWillingnessAdjustment,adjustedShotProbability)
                    adjustedShotProbability -= playerShotWillingnessTransfer
                    if availableAdjustedMovePassProbability > 0:
                        adjustedMoveProbability += playerShotWillingnessTransfer * (adjustedMoveProbability / availableAdjustedMovePassProbability)
                        adjustedPassProbability += playerShotWillingnessTransfer * (adjustedPassProbability / availableAdjustedMovePassProbability)
                    else:
                        adjustedMoveProbability += playerShotWillingnessTransfer / 2
                        adjustedPassProbability += playerShotWillingnessTransfer / 2

            adjustedStealCutoff = baseStealProbability
            adjustedTurnoverCutoff = adjustedStealCutoff + baseTurnoverProbability
            adjustedMoveCutoff = adjustedTurnoverCutoff + adjustedMoveProbability
            adjustedPassCutoff = adjustedMoveCutoff + adjustedPassProbability

            actionRoll = random.random()
            if actionRoll < adjustedStealCutoff:
                action = "steal"
            elif actionRoll < adjustedTurnoverCutoff:
                action = "turnover"
            elif actionRoll < adjustedMoveCutoff:
                action = "move"
            elif actionRoll < adjustedPassCutoff:
                action = "pass"
            else:
                action = "shot"

            if attemptFinalHeave:
                action = "heave"

            if currShotClock <= offenseShotClockUrgencyStart and not attemptFinalHeave:
                print(f"Shot-clock urgency: {currShotClock:.1f}s | Pace: {offensePace} | Urgency begins: {offenseShotClockUrgencyStart:.1f}s | BBIQ: {shotClockBBIQ:.0f} | Awareness modifier: {shotClockAwarenessModifier:.3f} | Progress: {shotClockUrgencyProgress:.3f} | Base shot chance: {baseShotProbability:.2%} | Requested bonus: {requestedShotClockUrgencyBonus:.2%} | Actual transfer: {shotClockUrgencyTransfer:.2%} | Adjusted shot chance: {adjustedShotProbability:.2%} | Roll: {actionRoll:.4f} | Action: {action.upper()}")

            if playerShotPreference is not None and not attemptFinalHeave:
                print(f"Shot preference: {preferenceZone} | Player: {playerShotPreference:.1f}% | Active lineup: {activeLineupPreferences[preferenceZone]:.1f}% | Requested adjustment: {playerShotWillingnessAdjustment:+.2%} | Actual transfer: {math.copysign(playerShotWillingnessTransfer,playerShotWillingnessAdjustment):+.2%} | Final shot chance: {adjustedShotProbability:.2%}")

            took_shot = False
            in_frontcourt = is_in_frontcourt(team_side, courtPos)

            if action == "shot" and (zone is None or not in_frontcourt):
                if crossed_midcourt:
                    action = "pass"
                else:
                    action = "move"

            if attemptFinalHeave:
                randTime = currTime
            else:
                paceActionTimeCategory = random.choices(paceActionTimeCategories,weights=paceActionTimeWeights[offensePace],k=1)[0]
                paceActionTimeModifier = paceActionTimeModifiers[paceActionTimeCategory]
                availableActionTime = max(0.0,min(currShotClock,currTime))
                minimumActionTime = max(0.25,0.439 * paceActionTimeModifier)
                maximumActionTime = 3.33 * paceActionTimeModifier
                if availableActionTime >= 2:
                    actionTimeUpperBound = min(maximumActionTime,availableActionTime)
                    actionTimeLowerBound = min(minimumActionTime,actionTimeUpperBound)
                    randTime = round(random.uniform(actionTimeLowerBound,actionTimeUpperBound),2)
                elif availableActionTime > 0.25:
                    randTime = round(min(availableActionTime,max(0.25,1.0 * paceActionTimeModifier)),2)
                else:
                    randTime = availableActionTime
            if attemptFinalHeave:
                elapsedTime = currTime
            else:
                roundedActionTime = round(randTime,2)
                elapsedTime = availableActionTime if roundedActionTime <= 0 < availableActionTime else min(availableActionTime,roundedActionTime)
            addPlayingTime(elapsedTime)
            teamPossessionTime[offense] += elapsedTime
            currTime = max(0.0,currTime - elapsedTime)
            currShotClock = max(0.0,currShotClock - elapsedTime)

            shotClockQualityAdjustment = 0.0
            shotClockQualityLabel = "normal window"
            if league == "CBB":
                if currShotClock >= 26:
                    shotClockQualityAdjustment = -0.020
                    shotClockQualityLabel = "extremely early"
                elif currShotClock >= 22:
                    shotClockQualityAdjustment = -0.010
                    shotClockQualityLabel = "early"
                elif currShotClock < 3:
                    shotClockQualityAdjustment = -0.015
                    shotClockQualityLabel = "desperation"
                elif currShotClock < 6:
                    shotClockQualityAdjustment = -0.005
                    shotClockQualityLabel = "late"
            else:
                if currShotClock >= 21:
                    shotClockQualityAdjustment = -0.020
                    shotClockQualityLabel = "extremely early"
                elif currShotClock >= 18:
                    shotClockQualityAdjustment = -0.010
                    shotClockQualityLabel = "early"
                elif currShotClock < 2.5:
                    shotClockQualityAdjustment = -0.015
                    shotClockQualityLabel = "desperation"
                elif currShotClock < 5:
                    shotClockQualityAdjustment = -0.005
                    shotClockQualityLabel = "late"

            if currTime < 60:
                game_clock_text = f"00:{max(0.0, currTime):04.1f}"
            else:
                display_game_time = max(0, math.ceil(currTime))
                display_minutes = display_game_time // 60
                display_seconds = display_game_time % 60
                game_clock_text = f"{display_minutes:02d}:{display_seconds:02d}"

            display_shot_clock = max(0.0, currShotClock)

            if display_shot_clock < 10:
                shot_clock_text = f"{display_shot_clock:04.1f}"
            else:
                shot_clock_text = f"{math.ceil(display_shot_clock):02d}"

            qtrminutes, qtrseconds = divmod(displayGameTime, 60)
            qtrhours, qtrminutes = divmod(qtrminutes, 60)

            shotminutes, shotseconds = divmod(displayShotClock, 60)
            shothours, shotminutes = divmod(shotminutes, 60)

            if action == "heave":
                currTime = 0
                currShotClock = 0
                assistPlayer = None
                took_shot = True

                if offense == t1:
                    heaveStats = t1stats
                else:
                    heaveStats = t2stats

                heaveShooterMinutes = float(heaveStats.at[possPlayer["id"].item(),"MP"]) / 60
                heaveRecoveryMinutes = getPlayerRecoveryMinutes(possPlayer)
                heaveFatigueMinutes = max(0.0,heaveShooterMinutes - heaveRecoveryMinutes)
                (heaveShootingRating,baseHeaveShootingRating,heaveStaminaCapacity,heaveShooterMinutes,heaveStaminaUsageRatio,heaveFatiguePenalty,heaveStaminaModifier,) = get_stamina_adjusted_rating(possPlayer,"shooting3",heaveShooterMinutes,heaveRecoveryMinutes)
                staminaAdjustedHeaveShootingRating = heaveShootingRating
                (heaveShootingRating,heaveMomentumStrength,heaveMomentumBonus,heaveMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedHeaveShootingRating,offense)

                normalHeaveThreeChance = (0.008 * heaveShootingRating) + 0.13
                if offense == t1:
                    normalHeaveThreeChance += HCAAdj
                heaveChance = max(finalHeaveMinimumChance,min(finalHeaveMaximumChance,normalHeaveThreeChance * finalHeaveDifficultyMultiplier))
                heaveRoll = random.random()
                heaveMade = (heaveRoll < heaveChance)

                if offense == t1:
                    t1stats.at[possPlayer["id"].item(),"3PT Shot Att",] += 1
                    t13a += 1
                else:
                    t2stats.at[possPlayer["id"].item(),"3PT Shot Att",] += 1
                    t23a += 1

                print(f"{possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} launches a desperation heave from beyond half court!")
                print(f"Final heave: shooting3 {heaveShootingRating:.4f} [base {baseHeaveShootingRating:.2f}; stamina adjusted {staminaAdjustedHeaveShootingRating:.4f}; MP {heaveShooterMinutes:.2f}; recovery {heaveRecoveryMinutes:.2f}; fatigue load {heaveFatigueMinutes:.2f}/{heaveStaminaCapacity:.2f}; stamina modifier {heaveStaminaModifier:.3f}; momentum {heaveMomentumStrength:.0%}; momentum bonus {heaveMomentumBonus:.2%}; momentum modifier {heaveMomentumModifier:.3f}] | Normal 3PT chance: {normalHeaveThreeChance:.2%} | Heave multiplier: {finalHeaveDifficultyMultiplier:.3f} | Heave chance: {heaveChance:.2%} | Roll: {heaveRoll:.4f}")

                if heaveMade:
                    if offense == t1:
                        t1pts += 3
                        t13m += 1
                        t1stats.at[possPlayer["id"].item(),"3PT Shot Made",] += 1
                        if period == 1:
                            t1q1pts += 3
                        elif period == 2:
                            t1q2pts += 3
                        elif league != "CBB" and period == 3:
                            t1q3pts += 3
                        elif league != "CBB" and period == 4:
                            t1q4pts += 3
                        elif period > periodPerGame:
                            t1qotpts += 3
                    else:
                        t2pts += 3
                        t23m += 1
                        t2stats.at[possPlayer["id"].item(),"3PT Shot Made",] += 1
                        if period == 1:
                            t2q1pts += 3
                        elif period == 2:
                            t2q2pts += 3
                        elif league != "CBB" and period == 3:
                            t2q3pts += 3
                        elif league != "CBB" and period == 4:
                            t2q4pts += 3
                        elif period > periodPerGame:
                            t2qotpts += 3

                    print("...GOOD! IT COUNTS AT THE BUZZER!")
                    adjustMomentum(offense,momentumMadeThreeSwing,"made final heave")
                else:
                    print("...OFF THE MARK! The horn sounds.")
                    adjustMomentum(defense,momentumMissSwing,"missed final heave")

            if zone is not None and in_frontcourt:
                if crossed_midcourt is False:
                    shoot_modifier = 0.5
                else:
                    shoot_modifier = 1.0

                if action == "shot":
                    zone = get_shot_zone(courtPos)
                    in_frontcourt = is_in_frontcourt(team_side, courtPos)
                    if zone is not None and in_frontcourt:
                        shootPlayer = possPlayer

                        if offense == t1:
                            offenseStats = t1stats
                            defenseStats = t2stats
                        else:
                            offenseStats = t2stats
                            defenseStats = t1stats

                        shootPlayerMinutes = float(offenseStats.at[shootPlayer["id"].item(),"MP"]) / 60
                        defenderMinutes = float(defenseStats.at[defender["id"].item(),"MP"]) / 60
                        shootPlayerRecoveryMinutes = getPlayerRecoveryMinutes(shootPlayer)
                        defenderRecoveryMinutes = getPlayerRecoveryMinutes(defender)
                        shootPlayerFatigueMinutes = max(0.0,shootPlayerMinutes - shootPlayerRecoveryMinutes)
                        defenderFatigueMinutes = max(0.0,defenderMinutes - defenderRecoveryMinutes)
                        (_,_,defenderStaminaCapacity,defenderMinutes,defenderStaminaUsageRatio,defenderFatiguePenalty,defenderStaminaModifier,) = get_stamina_adjusted_rating(defender,"perimeter_defense",defenderMinutes,defenderRecoveryMinutes)
                        baseBlockRating = float(defender["block"])

                        if zone in ["three", "corner_three"]:
                            shotOffenseType = "shooting3"
                            (shotOffense, baseShotOffense, shooterStaminaCapacity, shootPlayerMinutes,shooterStaminaUsageRatio, shooterFatiguePenalty,shooterStaminaModifier,) = get_stamina_adjusted_rating(shootPlayer, shotOffenseType,shootPlayerMinutes,shootPlayerRecoveryMinutes)
                            staminaAdjustedShotOffense = shotOffense
                            (shotOffense,shotMomentumStrength,shotMomentumBonus,shotMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedShotOffense,offense)
                            baseShotChance = (0.008 * shotOffense) + 0.180
                            if offense == t1:
                                baseShotChance += HCAAdj
                            (shotDefenseAdjustment,shotDefense,shotDefenseType,) = get_shot_defense_adjustment(defender,courtPos,defenderStaminaModifier)
                            madeShot = max(0.0,min(1.0,baseShotChance + shotDefenseAdjustment + shotClockQualityAdjustment + doubleTeamShotAdjustment))

                            (shootingFoulChance,zoneFoulBaseline,foulDefenderIQ,bbiqFoulModifier,) = get_shooting_foul_chance(defender,courtPos)
                            shootingFoulRoll = random.random()
                            shootingFoul = (shootingFoulRoll < shootingFoulChance)
                            defenderFouledOut = False
                            defenderFoulProtected = False
                            if shootingFoul:

                                defenderStatId = defender["id"].item()
                                defenderPlayerId = int(defender["player_id"])

                                if offense == t1:
                                    t2stats.at[defenderStatId,"Foul",] += 1
                                    if period == 1:
                                        t2FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t2FirstHalfTeamFouls
                                    else:
                                        t2SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t2SecondHalfTeamFouls

                                    defenderFoulTotal = int(t2stats.at[defenderStatId,"Foul"])
                                    if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t2FouledOutPlayerIds:
                                        t2FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = registerFoulProtection(2,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")
                                else:
                                    t1stats.at[defenderStatId,"Foul",] += 1
                                    if period == 1:
                                        t1FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t1FirstHalfTeamFouls
                                    else:
                                        t1SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t1SecondHalfTeamFouls

                                    defenderFoulTotal = int(t1stats.at[defenderStatId,"Foul"])
                                    if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t1FouledOutPlayerIds:
                                        t1FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = registerFoulProtection(1,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")
                                print(f"Defending team fouls this half: {defendingHalfTeamFouls}")

                                if defenderFouledOut:
                                    print(f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!")

                                blockChance = 0
                                zoneBlockBaseline = 0
                                blockRating = baseBlockRating * defenderStaminaModifier
                                blockRatingAdjustment = 0
                                defenderHeight = float(defender["height"])
                                shooterHeight = float(shootPlayer["height"])
                                heightAdjustment = 0
                                blockRoll = None
                                shotBlocked = False
                            else:
                                (blockChance, zoneBlockBaseline, blockRating, blockRatingAdjustment, defenderHeight,
                                 shooterHeight, heightAdjustment,) = get_block_chance(defender, shootPlayer, courtPos,
                                                                                      defenderStaminaModifier)
                                blockRoll = random.random()
                                shotBlocked = (blockRoll < blockChance)

                            if shotBlocked:
                                shotRand = None
                            else:
                                shotRand = random.random()

                            if shootingFoul:
                                madeShot *= shootingFoulMadeShotModifier
                            shotMade = (not shotBlocked and shotRand < madeShot)
                            shotRollText = ("SKIPPED" if shotRand is None else f"{shotRand:.4f}")
                            print(f"Shot offense: {shotOffense:.4f} [{shotOffenseType}; base {baseShotOffense:.2f}; stamina adjusted {staminaAdjustedShotOffense:.4f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; stamina modifier {shooterStaminaModifier:.3f}; momentum {shotMomentumStrength:.0%}; momentum bonus {shotMomentumBonus:.2%}; momentum modifier {shotMomentumModifier:.3f}] | Shot defense: {shotDefense:.4f} [{shotDefenseType}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Defense adjustment: {shotDefenseAdjustment:+.2%} | Shot-clock quality: {shotClockQualityLabel} {shotClockQualityAdjustment:+.2%} | Double-team role: {doubleTeamRole} {doubleTeamShotAdjustment:+.2%} | Final shot chance: {madeShot:.2%} | Roll: {shotRollText}")
                            blockRollText = ("SKIPPED" if blockRoll is None else f"{blockRoll:.4f}")

                            print(
                                f"Shooting foul baseline: {zoneFoulBaseline:.2%} | "
                                f"Defender BBIQ: {foulDefenderIQ:.0f} | "
                                f"BBIQ modifier: {bbiqFoulModifier:.3f} | "
                                f"Foul chance: {shootingFoulChance:.2%} | "
                                f"Foul roll: {shootingFoulRoll:.4f} | "
                                f"{'FOUL' if shootingFoul else 'NO FOUL'}"
                            )

                            print(
                                f"Block rating: {blockRating:.4f} [base {baseBlockRating:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; modifier {defenderStaminaModifier:.3f}] | "
                                f"Zone baseline: {zoneBlockBaseline:.2%} | "
                                f"Rating adjustment: "
                                f"{blockRatingAdjustment:+.2%} | "
                                f"Height: {defenderHeight:.0f} vs "
                                f"{shooterHeight:.0f} | "
                                f"Height adjustment: "
                                f"{heightAdjustment:+.2%} | "
                                f"Block chance: {blockChance:.2%} | "
                                f"Block roll: {blockRollText} | "
                                f"{'BLOCKED' if shotBlocked else 'NOT BLOCKED'}"
                            )

                            if not shootingFoul or shotMade:
                                if offense == t1:
                                    t1stats.at[shootPlayer["id"].item(), "3PT Shot Att",] += 1
                                    t13a += 1
                                else:
                                    t2stats.at[shootPlayer["id"].item(), "3PT Shot Att",] += 1
                                    t23a += 1

                            print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                            print(f"3-point attempt from {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']}")
                            if shotMade:
                                if offense == t1:
                                    t1pts += 3
                                    t13m += 1
                                    t1stats.at[shootPlayer["id"].item(),"3PT Shot Made",] += 1
                                    if assistPlayer is not None: t1stats.at[assistPlayer["id"].item(),"Assist",] += 1
                                    if period == 1:
                                        t1q1pts += 3
                                    elif period == 2:
                                        t1q2pts += 3
                                    elif league != "CBB" and period == 3:
                                        t1q3pts += 3
                                    elif league != "CBB" and period == 4:
                                        t1q4pts += 3
                                    elif period > periodPerGame:
                                        t1qotpts += 3
                                else:
                                    t2pts += 3
                                    t23m += 1
                                    t2stats.at[shootPlayer["id"].item(),"3PT Shot Made",] += 1
                                    if assistPlayer is not None: t2stats.at[assistPlayer["id"].item(),"Assist",] += 1
                                    if period == 1:
                                        t2q1pts += 3
                                    elif period == 2:
                                        t2q2pts += 3
                                    elif league != "CBB" and period == 3:
                                        t2q3pts += 3
                                    elif league != "CBB" and period == 4:
                                        t2q4pts += 3
                                    elif period > periodPerGame:
                                        t2qotpts += 3

                                if assistPlayer is not None:
                                    print("...GOOD! Assisted by " + assistPlayer["position"] + " " + assistPlayer["first_name"] + " " + assistPlayer["last_name"])
                                else:
                                    print("...GOOD!")
                                adjustMomentum(offense,momentumMadeThreeSwing,"made three-point shot")
                            else:
                                if shotBlocked:
                                    if offense == t1:
                                        t2stats.at[defender["id"].item(),"Blk",] += 1
                                    else:
                                        t1stats.at[defender["id"].item(),"Blk",] += 1
                                    print(f"...BLOCKED by {defender['position']} {defender['first_name']} {defender['last_name']}!")
                                    adjustMomentum(defense,momentumBlockSwing,"blocked three-point shot")
                                elif shootingFoul:
                                    print("...MISSED, but a shooting foul is called!")
                                    adjustMomentum(defense,momentumMissSwing,"missed three-point shot")
                                else:
                                    print("...MISSED!")
                                    adjustMomentum(defense,momentumMissSwing,"missed three-point shot")

                            assistPlayer = None
                            freeThrowsAwarded = 0
                            lastFreeThrowMade = False
                            if shootingFoul:
                                freeThrowsAwarded = 1 if shotMade else 3
                                print(f"FOUL on {defender['position']} {defender['first_name']} {defender['last_name']}! {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} will shoot {freeThrowsAwarded} free throw{'s' if freeThrowsAwarded != 1 else ''}.")
                                shootingFoulMediaTimeoutTaken = checkTimeoutStoppage(offense,True,shootPlayer)
                                freeThrowSubsCompleted = shootingFoulMediaTimeoutTaken
                                if (defenderFouledOut or defenderFoulProtected) and not freeThrowSubsCompleted:
                                    pullFreeThrowSubs(shootPlayer)
                                    freeThrowSubsCompleted = True
                                    defendedPlayerId = None
                                    currentDefender = None
                                    previousDefender = None
                                elif freeThrowsAwarded == 1 and not freeThrowSubsCompleted:
                                    pullFreeThrowSubs(shootPlayer)
                                    freeThrowSubsCompleted = True
                                if offense == t1:
                                    offense_df = t1onCourt
                                    defense_df = t2onCourt
                                    freeThrowStats = t1stats
                                else:
                                    offense_df = t2onCourt
                                    defense_df = t1onCourt
                                    freeThrowStats = t2stats

                                shootPlayerMinutes = float(freeThrowStats.at[shootPlayer["id"].item(),"MP"]) / 60
                                shootPlayerRecoveryMinutes = getPlayerRecoveryMinutes(shootPlayer)
                                shootPlayerFatigueMinutes = max(0.0,shootPlayerMinutes - shootPlayerRecoveryMinutes)
                                (_,_,shooterStaminaCapacity,shootPlayerMinutes,shooterStaminaUsageRatio,shooterFatiguePenalty,shooterStaminaModifier,) = get_stamina_adjusted_rating(shootPlayer,"free_throw",shootPlayerMinutes,shootPlayerRecoveryMinutes)
                                freeThrowHCAAdjustment = HCAAdj if offense == t1 else 0

                                for freeThrowNumber in range(1,freeThrowsAwarded + 1):
                                    (freeThrowMade, freeThrowChance, freeThrowRoll, freeThrowRating,
                                     baseFreeThrowRating,) = resolve_free_throw(shootPlayer, freeThrowHCAAdjustment,
                                                                                shooterStaminaModifier)

                                    if offense == t1:
                                        t1stats.at[shootPlayer["id"].item(),"FT Shot Att",] += 1
                                    else:
                                        t2stats.at[shootPlayer["id"].item(),"FT Shot Att",] += 1

                                    if freeThrowMade:
                                        if offense == t1:
                                            t1pts += 1
                                            t1stats.at[shootPlayer["id"].item(),"FT Shot Made",] += 1
                                            if period == 1:
                                                t1q1pts += 1
                                            elif period == 2:
                                                t1q2pts += 1
                                            elif league != "CBB" and period == 3:
                                                t1q3pts += 1
                                            elif league != "CBB" and period == 4:
                                                t1q4pts += 1
                                            elif period > periodPerGame:
                                                t1qotpts += 1
                                        else:
                                            t2pts += 1
                                            t2stats.at[shootPlayer["id"].item(),"FT Shot Made",] += 1
                                            if period == 1:
                                                t2q1pts += 1
                                            elif period == 2:
                                                t2q2pts += 1
                                            elif league != "CBB" and period == 3:
                                                t2q3pts += 1
                                            elif league != "CBB" and period == 4:
                                                t2q4pts += 1
                                            elif period > periodPerGame:
                                                t2qotpts += 1

                                    print(f"Free throw {freeThrowNumber} of {freeThrowsAwarded}: rating {freeThrowRating:.4f} [base {baseFreeThrowRating:.2f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; modifier {shooterStaminaModifier:.3f}] | Chance: {freeThrowChance:.2%} | Roll: {freeThrowRoll:.4f} | {'GOOD' if freeThrowMade else 'MISSED'}")
                                    lastFreeThrowMade = freeThrowMade
                                    if freeThrowNumber == 1 and freeThrowsAwarded > 1 and not freeThrowSubsCompleted:
                                        pullFreeThrowSubs(shootPlayer)
                                        freeThrowSubsCompleted = True
                                        if offense == t1:
                                            offense_df = t1onCourt
                                            defense_df = t2onCourt
                                        else:
                                            offense_df = t2onCourt
                                            defense_df = t1onCourt

                            needsRebound = ((not shootingFoul and not shotMade) or (shootingFoul and not lastFreeThrowMade))

                            if needsRebound:
                                rebRand = random.random()
                                if offense == t1:
                                    offensiveReboundChance = lineupParameters["t1OffensiveRebound"]
                                else:
                                    offensiveReboundChance = lineupParameters["t2OffensiveRebound"]

                                if rebRand < offensiveReboundChance:
                                    pickRebounder = random.choice(list(offense_df.values()))
                                    while pickRebounder["id"] == shootPlayer["id"]:
                                        pickRebounder = random.choice(list(offense_df.values()))
                                    possPlayer = pickRebounder
                                    if offense == t1:
                                        t1stats.at[possPlayer["id"].item(),"OREB",] += 1
                                    else:
                                        t2stats.at[possPlayer["id"].item(),"OREB",] += 1
                                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the offensive rebound for " + possTeam)
                                    currShotClock = shotClockReset
                                    if currTime < currShotClock:
                                        currShotClock = currTime
                                else:
                                    possPlayer = random.choice(list(defense_df.values()))
                                    if offense == t1:
                                        t2stats.at[possPlayer["id"].item(),"DREB",] += 1
                                        possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = t2onCourt
                                        defense_df = t1onCourt
                                        courtPos = (random.randint(2,4),random.randint(2,4))
                                    else:
                                        t1stats.at[possPlayer["id"].item(),"DREB",] += 1
                                        possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = t1onCourt
                                        defense_df = t2onCourt
                                        courtPos = (random.randint(2,4) * -1,random.randint(2,4))
                                    currShotClock = shotClock
                                    if currTime <= shotClock:
                                        currShotClock = currTime
                                    crossed_midcourt = False
                                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the defensive rebound for " + possTeam)
                                    defendedPlayerId = None
                                    currentDefender = None
                                    previousDefender = None
                            else:
                                if offense == t1:
                                    possTeam = t2
                                    offense = t2
                                    defense = t1
                                    offense_df = t2onCourt
                                    defense_df = t1onCourt
                                    courtPos = (4,3)
                                    possPlayer = random.choice(list(t2onCourt.values()))
                                else:
                                    possTeam = t1
                                    offense = t1
                                    defense = t2
                                    offense_df = t1onCourt
                                    defense_df = t2onCourt
                                    courtPos = (-4,3)
                                    possPlayer = random.choice(list(t1onCourt.values()))

                                crossed_midcourt = False
                                currShotClock = shotClock
                                if currTime <= shotClock:
                                    currShotClock = currTime
                                print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out for " + possTeam)
                                finalHeavePending = True
                                defendedPlayerId = None
                                currentDefender = None
                                previousDefender = None

                            print(t1 + ": " + str(t1pts) + " / " + t2 + ": " + str(t2pts))
                            print(footerPos)
                            printMomentumMeter()
                            took_shot = True

                        elif zone in ["inside","paint","midrange",]:
                            if zone == "midrange":
                                shotOffenseType = "shooting2"
                                (shotOffense,baseShotOffense,shooterStaminaCapacity,shootPlayerMinutes,shooterStaminaUsageRatio,shooterFatiguePenalty,shooterStaminaModifier,) = get_stamina_adjusted_rating(shootPlayer,shotOffenseType,shootPlayerMinutes,shootPlayerRecoveryMinutes)
                                staminaAdjustedShotOffense = shotOffense
                                (shotOffense,shotMomentumStrength,shotMomentumBonus,shotMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedShotOffense,offense)
                                baseShotChance = (0.0074 * shotOffense) + 0.265
                            else:
                                shotOffenseType = "finishing"
                                (shotOffense,baseShotOffense,shooterStaminaCapacity,shootPlayerMinutes,shooterStaminaUsageRatio,shooterFatiguePenalty,shooterStaminaModifier,) = get_stamina_adjusted_rating(shootPlayer,shotOffenseType,shootPlayerMinutes,shootPlayerRecoveryMinutes)
                                staminaAdjustedShotOffense = shotOffense
                                (shotOffense,shotMomentumStrength,shotMomentumBonus,shotMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedShotOffense,offense)
                                baseShotChance = (0.011 * shotOffense) + 0.39
                            if offense == t1:
                                baseShotChance += HCAAdj
                            (shotDefenseAdjustment,shotDefense,shotDefenseType,) = get_shot_defense_adjustment(defender,courtPos,defenderStaminaModifier)
                            madeShot = max(0.0,min(1.0,baseShotChance + shotDefenseAdjustment + shotClockQualityAdjustment + doubleTeamShotAdjustment))

                            (shootingFoulChance,zoneFoulBaseline,foulDefenderIQ,bbiqFoulModifier,) = get_shooting_foul_chance(defender,courtPos)
                            shootingFoulRoll = random.random()
                            shootingFoul = (shootingFoulRoll < shootingFoulChance)
                            defenderFouledOut = False
                            defenderFoulProtected = False

                            if shootingFoul:
                                defenderStatId = defender["id"].item()
                                defenderPlayerId = int(defender["player_id"])

                                if offense == t1:
                                    t2stats.at[defenderStatId,"Foul",] += 1
                                    if period == 1:
                                        t2FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t2FirstHalfTeamFouls
                                    else:
                                        t2SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t2SecondHalfTeamFouls

                                    defenderFoulTotal = int(t2stats.at[defenderStatId,"Foul"])
                                    if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t2FouledOutPlayerIds:
                                        t2FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = registerFoulProtection(2,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")
                                else:
                                    t1stats.at[defenderStatId,"Foul",] += 1
                                    if period == 1:
                                        t1FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t1FirstHalfTeamFouls
                                    else:
                                        t1SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = t1SecondHalfTeamFouls

                                    defenderFoulTotal = int(t1stats.at[defenderStatId,"Foul"])
                                    if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t1FouledOutPlayerIds:
                                        t1FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = registerFoulProtection(1,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")
                                print(f"Defending team fouls this half: {defendingHalfTeamFouls}")

                                if defenderFouledOut:
                                    print(f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!")

                                blockChance = 0
                                zoneBlockBaseline = 0
                                blockRating = baseBlockRating * defenderStaminaModifier
                                blockRatingAdjustment = 0
                                defenderHeight = float(defender["height"])
                                shooterHeight = float(shootPlayer["height"])
                                heightAdjustment = 0
                                blockRoll = None
                                shotBlocked = False
                            else:
                                (blockChance, zoneBlockBaseline, blockRating, blockRatingAdjustment, defenderHeight,
                                 shooterHeight, heightAdjustment,) = get_block_chance(defender, shootPlayer, courtPos,
                                                                                      defenderStaminaModifier)
                                blockRoll = random.random()
                                shotBlocked = (blockRoll < blockChance)

                            if shotBlocked:
                                shotRand = None
                            else:
                                shotRand = random.random()

                            if shootingFoul:
                                madeShot *= shootingFoulMadeShotModifier
                            shotMade = (not shotBlocked and shotRand < madeShot)
                            shotRollText = ("SKIPPED" if shotRand is None else f"{shotRand:.4f}")
                            print(f"Shot offense: {shotOffense:.4f} [{shotOffenseType}; base {baseShotOffense:.2f}; stamina adjusted {staminaAdjustedShotOffense:.4f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; stamina modifier {shooterStaminaModifier:.3f}; momentum {shotMomentumStrength:.0%}; momentum bonus {shotMomentumBonus:.2%}; momentum modifier {shotMomentumModifier:.3f}] | Shot defense: {shotDefense:.4f} [{shotDefenseType}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Defense adjustment: {shotDefenseAdjustment:+.2%} | Shot-clock quality: {shotClockQualityLabel} {shotClockQualityAdjustment:+.2%} | Double-team role: {doubleTeamRole} {doubleTeamShotAdjustment:+.2%} | Final shot chance: {madeShot:.2%} | Roll: {shotRollText}")
                            blockRollText = ("SKIPPED" if blockRoll is None else f"{blockRoll:.4f}")

                            print(
                                f"Shooting foul baseline: {zoneFoulBaseline:.2%} | "
                                f"Defender BBIQ: {foulDefenderIQ:.0f} | "
                                f"BBIQ modifier: {bbiqFoulModifier:.3f} | "
                                f"Foul chance: {shootingFoulChance:.2%} | "
                                f"Foul roll: {shootingFoulRoll:.4f} | "
                                f"{'FOUL' if shootingFoul else 'NO FOUL'}"
                            )

                            print(
                                f"Block rating: {blockRating:.4f} [base {baseBlockRating:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; modifier {defenderStaminaModifier:.3f}] | "
                                f"Zone baseline: {zoneBlockBaseline:.2%} | "
                                f"Rating adjustment: "
                                f"{blockRatingAdjustment:+.2%} | "
                                f"Height: {defenderHeight:.0f} vs "
                                f"{shooterHeight:.0f} | "
                                f"Height adjustment: "
                                f"{heightAdjustment:+.2%} | "
                                f"Block chance: {blockChance:.2%} | "
                                f"Block roll: {blockRollText} | "
                                f"{'BLOCKED' if shotBlocked else 'NOT BLOCKED'}"
                            )

                            if not shootingFoul or shotMade:
                                if offense == t1:
                                    t12a += 1
                                    if zone == "midrange":
                                        t1stats.at[shootPlayer["id"].item(),"Mid Shot Att",] += 1
                                    else:
                                        t1stats.at[shootPlayer["id"].item(),"Ins Shot Att",] += 1
                                else:
                                    t22a += 1
                                    if zone == "midrange":
                                        t2stats.at[shootPlayer["id"].item(),"Mid Shot Att",] += 1
                                    else:
                                        t2stats.at[shootPlayer["id"].item(),"Ins Shot Att",] += 1

                            print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                            print(f"2-point attempt from {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']}")

                            if shotMade:
                                madeShotResult = "normal"
                                shotMakeQuality = shotRand / madeShot

                                if zone == "inside" and shotMakeQuality < insideDunkThreshold:
                                    madeShotResult = "inside_dunk"
                                elif zone == "paint":
                                    if shotMakeQuality < paintPosterDunkThreshold:
                                        madeShotResult = "paint_poster_dunk"
                                    elif shotMakeQuality < paintDriveDunkThreshold:
                                        madeShotResult = "paint_drive_dunk"

                                if offense == t1:
                                    t1pts += 2
                                    t12m += 1
                                    if zone == "midrange":
                                        t1stats.at[shootPlayer["id"].item(),"Mid Shot Made",] += 1
                                    else:
                                        t1stats.at[shootPlayer["id"].item(),"Ins Shot Made",] += 1
                                    if assistPlayer is not None: t1stats.at[assistPlayer["id"].item(),"Assist",] += 1
                                    if period == 1:
                                        t1q1pts += 2
                                    elif period == 2:
                                        t1q2pts += 2
                                    elif league != "CBB" and period == 3:
                                        t1q3pts += 2
                                    elif league != "CBB" and period == 4:
                                        t1q4pts += 2
                                    elif period > periodPerGame:
                                        t1qotpts += 2
                                else:
                                    t2pts += 2
                                    t22m += 1
                                    if zone == "midrange":
                                        t2stats.at[shootPlayer["id"].item(),"Mid Shot Made",] += 1
                                    else:
                                        t2stats.at[shootPlayer["id"].item(),"Ins Shot Made",] += 1
                                    if assistPlayer is not None: t2stats.at[assistPlayer["id"].item(),"Assist",] += 1
                                    if period == 1:
                                        t2q1pts += 2
                                    elif period == 2:
                                        t2q2pts += 2
                                    elif league != "CBB" and period == 3:
                                        t2q3pts += 2
                                    elif league != "CBB" and period == 4:
                                        t2q4pts += 2
                                    elif period > periodPerGame:
                                        t2qotpts += 2

                                assistText = ""
                                if assistPlayer is not None:
                                    assistText = f" Assisted by {assistPlayer['position']} {assistPlayer['first_name']} {assistPlayer['last_name']}."

                                if madeShotResult == "inside_dunk":
                                    print(f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} slams it home!{assistText}")
                                elif madeShotResult == "paint_poster_dunk":
                                    print(f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} drives forward and POSTERIZES {defender['position']} {defender['first_name']} {defender['last_name']}! THE DISRESPECT!{assistText}")
                                elif madeShotResult == "paint_drive_dunk":
                                    print(f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} drives forward and throws it down!{assistText}")
                                elif assistPlayer is not None:
                                    print(f"...GOOD! Assisted by {assistPlayer['position']} {assistPlayer['first_name']} {assistPlayer['last_name']}")
                                else:
                                    print("...GOOD!")
                                if madeShotResult in ("inside_dunk","paint_drive_dunk"):
                                    adjustMomentum(offense,momentumDunkSwing,"made dunk")
                                elif madeShotResult == "paint_poster_dunk":
                                    adjustMomentum(offense,momentumPosterDunkSwing,"poster dunk")
                                else:
                                    adjustMomentum(offense,momentumMadeTwoSwing,"made two-point shot")
                            else:
                                if shotBlocked:
                                    if offense == t1:
                                        t2stats.at[defender["id"].item(),"Blk",] += 1
                                    else:
                                        t1stats.at[defender["id"].item(),"Blk",] += 1
                                    print(f"...BLOCKED by {defender['position']} {defender['first_name']} {defender['last_name']}!")
                                    adjustMomentum(defense,momentumBlockSwing,"blocked two-point shot")
                                elif shootingFoul:
                                    print("...MISSED, but a shooting foul is called!")
                                    adjustMomentum(defense,momentumMissSwing,"missed two-point shot")
                                else:
                                    print("...MISSED!")
                                    adjustMomentum(defense,momentumMissSwing,"missed two-point shot")

                            assistPlayer = None
                            freeThrowsAwarded = 0
                            lastFreeThrowMade = False

                            if shootingFoul:
                                freeThrowsAwarded = 1 if shotMade else 2
                                print(f"FOUL on {defender['position']} {defender['first_name']} {defender['last_name']}! {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} will shoot {freeThrowsAwarded} free throw{'s' if freeThrowsAwarded != 1 else ''}.")
                                shootingFoulMediaTimeoutTaken = checkTimeoutStoppage(offense,True,shootPlayer)
                                freeThrowSubsCompleted = shootingFoulMediaTimeoutTaken
                                if (defenderFouledOut or defenderFoulProtected) and not freeThrowSubsCompleted:
                                    pullFreeThrowSubs(shootPlayer)
                                    freeThrowSubsCompleted = True
                                    defendedPlayerId = None
                                    currentDefender = None
                                    previousDefender = None
                                elif freeThrowsAwarded == 1 and not freeThrowSubsCompleted:
                                    pullFreeThrowSubs(shootPlayer)
                                    freeThrowSubsCompleted = True
                                if offense == t1:
                                    offense_df = t1onCourt
                                    defense_df = t2onCourt
                                    freeThrowStats = t1stats
                                else:
                                    offense_df = t2onCourt
                                    defense_df = t1onCourt
                                    freeThrowStats = t2stats

                                shootPlayerMinutes = float(freeThrowStats.at[shootPlayer["id"].item(),"MP"]) / 60
                                shootPlayerRecoveryMinutes = getPlayerRecoveryMinutes(shootPlayer)
                                shootPlayerFatigueMinutes = max(0.0,shootPlayerMinutes - shootPlayerRecoveryMinutes)
                                (_,_,shooterStaminaCapacity,shootPlayerMinutes,shooterStaminaUsageRatio,shooterFatiguePenalty,shooterStaminaModifier,) = get_stamina_adjusted_rating(shootPlayer,"free_throw",shootPlayerMinutes,shootPlayerRecoveryMinutes)
                                freeThrowHCAAdjustment = HCAAdj if offense == t1 else 0

                                for freeThrowNumber in range(1,freeThrowsAwarded + 1):
                                    (freeThrowMade, freeThrowChance, freeThrowRoll, freeThrowRating,
                                     baseFreeThrowRating,) = resolve_free_throw(shootPlayer, freeThrowHCAAdjustment,
                                                                                shooterStaminaModifier)

                                    if offense == t1:
                                        t1stats.at[shootPlayer["id"].item(),"FT Shot Att",] += 1
                                    else:
                                        t2stats.at[shootPlayer["id"].item(),"FT Shot Att",] += 1

                                    if freeThrowMade:
                                        if offense == t1:
                                            t1pts += 1
                                            t1stats.at[shootPlayer["id"].item(),"FT Shot Made",] += 1
                                            if period == 1:
                                                t1q1pts += 1
                                            elif period == 2:
                                                t1q2pts += 1
                                            elif league != "CBB" and period == 3:
                                                t1q3pts += 1
                                            elif league != "CBB" and period == 4:
                                                t1q4pts += 1
                                            elif period > periodPerGame:
                                                t1qotpts += 1
                                        else:
                                            t2pts += 1
                                            t2stats.at[shootPlayer["id"].item(),"FT Shot Made",] += 1
                                            if period == 1:
                                                t2q1pts += 1
                                            elif period == 2:
                                                t2q2pts += 1
                                            elif league != "CBB" and period == 3:
                                                t2q3pts += 1
                                            elif league != "CBB" and period == 4:
                                                t2q4pts += 1
                                            elif period > periodPerGame:
                                                t2qotpts += 1

                                    print(f"Free throw {freeThrowNumber} of {freeThrowsAwarded}: rating {freeThrowRating:.4f} [base {baseFreeThrowRating:.2f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; modifier {shooterStaminaModifier:.3f}] | Chance: {freeThrowChance:.2%} | Roll: {freeThrowRoll:.4f} | {'GOOD' if freeThrowMade else 'MISSED'}")
                                    lastFreeThrowMade = freeThrowMade
                                    if freeThrowNumber == 1 and freeThrowsAwarded > 1 and not freeThrowSubsCompleted:
                                        pullFreeThrowSubs(shootPlayer)
                                        freeThrowSubsCompleted = True
                                        if offense == t1:
                                            offense_df = t1onCourt
                                            defense_df = t2onCourt
                                        else:
                                            offense_df = t2onCourt
                                            defense_df = t1onCourt

                            needsRebound = ((not shootingFoul and not shotMade) or (shootingFoul and not lastFreeThrowMade))
                            if needsRebound:
                                rebRand = random.random()
                                if offense == t1:
                                    offensiveReboundChance = lineupParameters["t1OffensiveRebound"]
                                else:
                                    offensiveReboundChance = lineupParameters["t2OffensiveRebound"]

                                if rebRand < offensiveReboundChance:
                                    possPlayer = random.choice(list(offense_df.values()))
                                    if offense == t1:
                                        t1stats.at[possPlayer["id"].item(),"OREB",] += 1
                                    else:
                                        t2stats.at[possPlayer["id"].item(),"OREB",] += 1
                                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the offensive rebound for " + possTeam)
                                    currShotClock = shotClockReset
                                    if currTime < currShotClock:
                                        currShotClock = currTime
                                else:
                                    possPlayer = random.choice(list(defense_df.values()))
                                    if offense == t1:
                                        t2stats.at[possPlayer["id"].item(),"DREB",] += 1
                                        possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = t2onCourt
                                        defense_df = t1onCourt
                                        courtPos = (random.randint(2,4),random.randint(2,4))
                                    else:
                                        t1stats.at[possPlayer["id"].item(),"DREB",] += 1
                                        possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = t1onCourt
                                        defense_df = t2onCourt
                                        courtPos = (random.randint(2,4) * -1,random.randint(2,4))

                                    currShotClock = shotClock
                                    if currTime <= shotClock:
                                        currShotClock = currTime
                                    crossed_midcourt = False
                                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the defensive rebound for " + possTeam)
                                    defendedPlayerId = None
                                    currentDefender = None
                                    previousDefender = None
                            else:
                                if offense == t1:
                                    possTeam = t2
                                    offense = t2
                                    defense = t1
                                    offense_df = t2onCourt
                                    defense_df = t1onCourt
                                    courtPos = (4,3)
                                    possPlayer = random.choice(list(t2onCourt.values()))
                                else:
                                    possTeam = t1
                                    offense = t1
                                    defense = t2
                                    offense_df = t1onCourt
                                    defense_df = t2onCourt
                                    courtPos = (-4,3)
                                    possPlayer = random.choice(list(t1onCourt.values()))

                                crossed_midcourt = False
                                currShotClock = shotClock
                                if currTime <= shotClock:
                                    currShotClock = currTime
                                print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out for " + possTeam)
                                finalHeavePending = True
                                defendedPlayerId = None
                                currentDefender = None
                                previousDefender = None

                            print(t1 + ": " + str(t1pts) + " / " + t2 + ": " + str(t2pts))
                            print(footerPos)
                            printMomentumMeter()
                            took_shot = True


            if took_shot is False:
                if currShotClock <= 0 and action != "shot" and currTime > 0:
                    print("Shot clock violation.")
                    checkTimeoutStoppage(defense,False)
                    assistPlayer = None
                    currShotClock = shotClock
                    if currTime <= shotClock:
                        currShotClock = currTime
                    crossed_midcourt = False
                    if offense == t1:
                        t1stats.at[possPlayer['id'].item(), 'TO'] += 1
                        takeoutPlayer = random.choice(list(t2onCourt.values()))
                        possPlayer = takeoutPlayer
                        possTeam = t2
                        offense = t2
                        defense = t1
                        offense_df = t2onCourt
                        defense_df = t1onCourt
                        courtPos = (4, 3)
                        print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes over for " + t2 + ".")
                    else:
                        t2stats.at[possPlayer['id'].item(), 'TO'] += 1
                        takeoutPlayer = random.choice(list(t1onCourt.values()))
                        possPlayer = takeoutPlayer
                        possTeam = t1
                        offense = t1
                        defense = t2
                        offense_df = t1onCourt
                        defense_df = t2onCourt
                        courtPos = (-4, 3)
                        print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes over for " + t1 + ".")
                    finalHeavePending = True

                else:
                    if action == "move":
                        if assistPlayer is not None:
                            assistMovementCount += 1
                            if assistMovementCount > 1:
                                assistPlayer = None
                                assistMovementCount = 0
                        formationDestinationWeights = t1FormationDestinationWeights if offense == t1 else t2FormationDestinationWeights
                        activeDestinationWeights,activeLineupPreferences = getActiveDestinationWeights(offense_df,formationDestinationWeights)
                        newPos = choose_weighted_move_spot(team_side,courtPos,crossed_midcourt,activeDestinationWeights)
                        if newPos is not None:
                            (offensiveFoulChance,offensiveFoulBaseline,offensivePlayerIQ,offensiveBBIQModifier,offensiveFoulDefenderIQ,offensiveFoulDefenderBBIQModifier,) = get_offensive_foul_chance(possPlayer,defender,newPos)
                            offensiveFoulRoll = random.random()
                            offensiveFoul = (offensiveFoulRoll < offensiveFoulChance)

                            print(
                                f"Offensive foul baseline: {offensiveFoulBaseline:.2%} | "
                                f"Offensive BBIQ: {offensivePlayerIQ:.0f} | "
                                f"Offensive modifier: {offensiveBBIQModifier:.3f} | "
                                f"Defender BBIQ: {offensiveFoulDefenderIQ:.0f} | "
                                f"Defender modifier: {offensiveFoulDefenderBBIQModifier:.3f} | "
                                f"Foul chance: {offensiveFoulChance:.2%} | "
                                f"Foul roll: {offensiveFoulRoll:.4f} | "
                                f"{'CHARGE' if offensiveFoul else 'NO OFFENSIVE FOUL'}"
                            )

                            if not offensiveFoul:
                                (nonShootingFoulChance,zoneFoulBaseline,foulDefenderIQ,bbiqFoulModifier,) = get_non_shooting_foul_chance(defender,newPos)
                                nonShootingFoulRoll = random.random()
                                nonShootingFoul = (nonShootingFoulRoll < nonShootingFoulChance)

                                print(
                                    f"Non-shooting foul baseline: {zoneFoulBaseline:.2%} | "
                                    f"Defender BBIQ: {foulDefenderIQ:.0f} | "
                                    f"BBIQ modifier: {bbiqFoulModifier:.3f} | "
                                    f"Foul chance: {nonShootingFoulChance:.2%} | "
                                    f"Foul roll: {nonShootingFoulRoll:.4f} | "
                                    f"{'FOUL' if nonShootingFoul else 'NO FOUL'}"
                                )
                                if not nonShootingFoul:
                                    offenseStats = t1stats if offense == t1 else t2stats
                                    defenseStats = t2stats if offense == t1 else t1stats

                                    possPlayerMinutes = float(offenseStats.at[possPlayer["id"].item(),"MP"]) / 60
                                    defenderMinutes = float(defenseStats.at[defender["id"].item(),"MP"]) / 60
                                    possPlayerRecoveryMinutes = getPlayerRecoveryMinutes(possPlayer)
                                    defenderRecoveryMinutes = getPlayerRecoveryMinutes(defender)
                                    possPlayerFatigueMinutes = max(0.0,possPlayerMinutes - possPlayerRecoveryMinutes)
                                    defenderFatigueMinutes = max(0.0,defenderMinutes - defenderRecoveryMinutes)

                                    (movementOffense,baseMovementOffense,offensiveStaminaCapacity,possPlayerMinutes,offensiveStaminaUsageRatio,offensiveFatiguePenalty,offensiveStaminaModifier,) = get_stamina_adjusted_rating(possPlayer,"agility",possPlayerMinutes,possPlayerRecoveryMinutes)
                                    movementOffenseType = "agility"
                                    staminaAdjustedMovementOffense = movementOffense
                                    (movementOffense,movementMomentumStrength,movementMomentumBonus,movementMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedMovementOffense,offense)

                                    (_,_,defenderStaminaCapacity,defenderMinutes,defenderStaminaUsageRatio,defenderFatiguePenalty,defenderStaminaModifier,) = get_stamina_adjusted_rating(defender,"perimeter_defense",defenderMinutes,defenderRecoveryMinutes)

                                    baseMovementDefense,movementDefenseType = get_movement_defense(defender,newPos)
                                    movementDefense,movementDefenseType = get_movement_defense(defender,newPos,defenderStaminaModifier)

                                    movementSuccessProbability = (
                                        get_movement_success_probability(
                                            movementOffense,
                                            movementDefense,
                                        )
                                    )
                                    movementSuccessProbability = max(0.10,min(0.90,movementSuccessProbability + doubleTeamMovementAdjustment))

                                    movementRoll = random.random()
                                    movementSuccessful = (
                                            movementRoll < movementSuccessProbability
                                    )

                                    print(f"Movement offense: {movementOffense:.4f} [{movementOffenseType}; base {baseMovementOffense:.2f}; stamina adjusted {staminaAdjustedMovementOffense:.4f}; MP {possPlayerMinutes:.2f}; recovery {possPlayerRecoveryMinutes:.2f}; fatigue load {possPlayerFatigueMinutes:.2f}/{offensiveStaminaCapacity:.2f}; stamina modifier {offensiveStaminaModifier:.3f}; momentum {movementMomentumStrength:.0%}; momentum bonus {movementMomentumBonus:.2%}; momentum modifier {movementMomentumModifier:.3f}] | Movement defense: {movementDefense:.4f} [{movementDefenseType}; base {baseMovementDefense:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Double-team role: {doubleTeamRole} {doubleTeamMovementAdjustment:+.2%} | Success chance: {movementSuccessProbability:.2%} | Roll: {movementRoll:.4f} | {'SUCCESS' if movementSuccessful else 'CUT OFF'} at {format_court_pos(newPos)}")

                                    if movementSuccessful:
                                        courtPos = newPos

                                        crossed_midcourt = update_crossed_midcourt(
                                            team_side,
                                            courtPos,
                                            crossed_midcourt,
                                        )
                                    print(
                                        (
                                            str(period) + pInd
                                            if period <= periodPerGame
                                            else "OT" + str(period - periodPerGame)
                                        )
                                        + ": "
                                        + game_clock_text
                                        + " / Shot Clock: :"
                                        + shot_clock_text
                                        + " ("
                                        + possTeam
                                        + ")"
                                    )

                                    if movementSuccessful:
                                        print(
                                            possPlayer["position"] + " "
                                            + possPlayer["first_name"] + " "
                                            + possPlayer["last_name"]
                                            + " moves the ball up the court for "
                                            + possTeam + "."
                                        )
                                    else:
                                        print(
                                            possPlayer["position"] + " "
                                            + possPlayer["first_name"] + " "
                                            + possPlayer["last_name"]
                                            + " is cut off and remains at "
                                            + format_court_pos(courtPos) + "."
                                        )
                                    print(footerPos)
                                    printMomentumMeter()
                                else:
                                    assistPlayer = None
                                    assistMovementCount = 0
                                    defenderFouledOut = False
                                    defenderFoulProtected = False
                                    defenderStatId = defender["id"].item()
                                    defenderPlayerId = int(defender["player_id"])

                                    if offense == t1:
                                        t2stats.at[defenderStatId,"Foul",] += 1
                                        if period == 1:
                                            t2FirstHalfTeamFouls += 1
                                            defendingHalfTeamFouls = t2FirstHalfTeamFouls
                                        else:
                                            t2SecondHalfTeamFouls += 1
                                            defendingHalfTeamFouls = t2SecondHalfTeamFouls

                                        defenderFoulTotal = int(t2stats.at[defenderStatId,"Foul"])
                                        if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t2FouledOutPlayerIds:
                                            t2FouledOutPlayerIds.add(defenderPlayerId)
                                            defenderFouledOut = True
                                        defenderFoulProtected = registerFoulProtection(2,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")
                                    else:
                                        t1stats.at[defenderStatId,"Foul",] += 1
                                        if period == 1:
                                            t1FirstHalfTeamFouls += 1
                                            defendingHalfTeamFouls = t1FirstHalfTeamFouls
                                        else:
                                            t1SecondHalfTeamFouls += 1
                                            defendingHalfTeamFouls = t1SecondHalfTeamFouls

                                        defenderFoulTotal = int(t1stats.at[defenderStatId,"Foul"])
                                        if defenderFoulTotal >= foulOutLimit and defenderPlayerId not in t1FouledOutPlayerIds:
                                            t1FouledOutPlayerIds.add(defenderPlayerId)
                                            defenderFouledOut = True
                                        defenderFoulProtected = registerFoulProtection(1,defenderStatId,defenderPlayerId,f"{defender['position']} {defender['first_name']} {defender['last_name']}")

                                    if league == "CBB" and defendingHalfTeamFouls >= 10:
                                        bonusType = "double_bonus"
                                    elif league == "CBB" and defendingHalfTeamFouls >= 7:
                                        bonusType = "one_and_one"
                                    else:
                                        bonusType = None

                                    print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                                    print(f"Non-shooting foul by {defender['position']} {defender['first_name']} {defender['last_name']} on {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']}!")
                                    print(f"Defending team fouls this half: {defendingHalfTeamFouls}")

                                    if defenderFouledOut:
                                        print(f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!")
                                    freeThrowsAwarded = 0
                                    lastFreeThrowMade = False

                                    if bonusType == "one_and_one":
                                        freeThrowsAwarded = 2
                                        print(f"{possTeam} is in the bonus. {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} will shoot one-and-one.")
                                    elif bonusType == "double_bonus":
                                        freeThrowsAwarded = 2
                                        print(f"{possTeam} is in the double bonus. {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} will shoot two free throws.")

                                    protectedFreeThrowPlayer = possPlayer if freeThrowsAwarded > 0 else None
                                    nonShootingFoulMediaTimeoutTaken = checkTimeoutStoppage(offense,True,protectedFreeThrowPlayer)
                                    freeThrowSubsCompleted = nonShootingFoulMediaTimeoutTaken
                                    if (defenderFouledOut or defenderFoulProtected) and freeThrowsAwarded > 0 and not freeThrowSubsCompleted:
                                        pullFreeThrowSubs(possPlayer)
                                        freeThrowSubsCompleted = True
                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None

                                    if offense == t1:
                                        offense_df = t1onCourt
                                        defense_df = t2onCourt
                                    else:
                                        offense_df = t2onCourt
                                        defense_df = t1onCourt

                                    if freeThrowsAwarded > 0:
                                        freeThrowHCAAdjustment = HCAAdj if offense == t1 else 0
                                        if offense == t1:
                                            freeThrowStats = t1stats
                                        else:
                                            freeThrowStats = t2stats
                                        freeThrowShooterMinutes = float(freeThrowStats.at[possPlayer["id"].item(),"MP"]) / 60
                                        freeThrowRecoveryMinutes = getPlayerRecoveryMinutes(possPlayer)
                                        freeThrowFatigueMinutes = max(0.0,freeThrowShooterMinutes - freeThrowRecoveryMinutes)
                                        (_,_,freeThrowStaminaCapacity,freeThrowShooterMinutes,freeThrowStaminaUsageRatio,freeThrowFatiguePenalty,freeThrowStaminaModifier,) = get_stamina_adjusted_rating(possPlayer,"free_throw",freeThrowShooterMinutes,freeThrowRecoveryMinutes)

                                        for freeThrowNumber in range(1,freeThrowsAwarded + 1):
                                            (freeThrowMade,freeThrowChance,freeThrowRoll,freeThrowRating,baseFreeThrowRating,) = resolve_free_throw(possPlayer,freeThrowHCAAdjustment,freeThrowStaminaModifier)

                                            if offense == t1:
                                                t1stats.at[possPlayer["id"].item(),"FT Shot Att",] += 1
                                            else:
                                                t2stats.at[possPlayer["id"].item(),"FT Shot Att",] += 1

                                            if freeThrowMade:
                                                if offense == t1:
                                                    t1pts += 1
                                                    t1stats.at[possPlayer["id"].item(),"FT Shot Made",] += 1
                                                    if period == 1:
                                                        t1q1pts += 1
                                                    elif period == 2:
                                                        t1q2pts += 1
                                                    elif league != "CBB" and period == 3:
                                                        t1q3pts += 1
                                                    elif league != "CBB" and period == 4:
                                                        t1q4pts += 1
                                                    elif period > periodPerGame:
                                                        t1qotpts += 1
                                                else:
                                                    t2pts += 1
                                                    t2stats.at[possPlayer["id"].item(),"FT Shot Made",] += 1
                                                    if period == 1:
                                                        t2q1pts += 1
                                                    elif period == 2:
                                                        t2q2pts += 1
                                                    elif league != "CBB" and period == 3:
                                                        t2q3pts += 1
                                                    elif league != "CBB" and period == 4:
                                                        t2q4pts += 1
                                                    elif period > periodPerGame:
                                                        t2qotpts += 1

                                            print(f"Free throw {freeThrowNumber} of {freeThrowsAwarded}: rating {freeThrowRating:.4f} [base {baseFreeThrowRating:.2f}; MP {freeThrowShooterMinutes:.2f}; recovery {freeThrowRecoveryMinutes:.2f}; fatigue load {freeThrowFatigueMinutes:.2f}/{freeThrowStaminaCapacity:.2f}; modifier {freeThrowStaminaModifier:.3f}] | Chance: {freeThrowChance:.2%} | Roll: {freeThrowRoll:.4f} | {'GOOD' if freeThrowMade else 'MISSED'}")
                                            lastFreeThrowMade = freeThrowMade

                                            if bonusType == "one_and_one" and freeThrowNumber == 1 and not freeThrowMade:
                                                print("The front end of the one-and-one is missed. The ball is live!")
                                                break
                                            if freeThrowNumber == 1 and freeThrowsAwarded > 1 and not freeThrowSubsCompleted:
                                                pullFreeThrowSubs(possPlayer)
                                                freeThrowSubsCompleted = True
                                                if offense == t1:
                                                    offense_df = t1onCourt
                                                    defense_df = t2onCourt
                                                else:
                                                    offense_df = t2onCourt
                                                    defense_df = t1onCourt
                                    if (defenderFouledOut or defenderFoulProtected) and freeThrowsAwarded == 0 and not nonShootingFoulMediaTimeoutTaken:
                                        t1onCourt,t2onCourt,lineupParameters = pullSubs(False)

                                        if offense == t1:
                                            offense_df = t1onCourt
                                            defense_df = t2onCourt
                                        else:
                                            offense_df = t2onCourt
                                            defense_df = t1onCourt

                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None
                                        substitutionReason = "foul-out" if defenderFouledOut else "foul protection"

                                        print(t1 + " Subs after " + substitutionReason + ":")
                                        for lineupPlayer in t1onCourt.values():
                                            print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])

                                        print(t2 + " Subs after " + substitutionReason + ":")
                                        for lineupPlayer in t2onCourt.values():
                                            print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])

                                    if bonusType is None:
                                        possPlayer = random.choice(list(offense_df.values()))
                                        currShotClock = max(currShotClock,shotClockReset)
                                        if currTime < currShotClock:
                                            currShotClock = currTime
                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None
                                        print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out for " + possTeam + ".")
                                        finalHeavePending = True

                                    elif not lastFreeThrowMade:
                                        rebRand = random.random()
                                        if offense == t1:
                                            offensiveReboundChance = lineupParameters["t1OffensiveRebound"]
                                        else:
                                            offensiveReboundChance = lineupParameters["t2OffensiveRebound"]

                                        if rebRand < offensiveReboundChance:
                                            possPlayer = random.choice(list(offense_df.values()))
                                            if offense == t1:
                                                t1stats.at[possPlayer["id"].item(),"OREB",] += 1
                                            else:
                                                t2stats.at[possPlayer["id"].item(),"OREB",] += 1
                                            print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the offensive rebound for " + possTeam)
                                            currShotClock = shotClockReset
                                            if currTime < currShotClock:
                                                currShotClock = currTime
                                        else:
                                            possPlayer = random.choice(list(defense_df.values()))
                                            if offense == t1:
                                                t2stats.at[possPlayer["id"].item(),"DREB",] += 1
                                                possTeam = t2
                                                offense = t2
                                                defense = t1
                                                offense_df = t2onCourt
                                                defense_df = t1onCourt
                                                courtPos = (random.randint(2,4),random.randint(2,4))
                                            else:
                                                t1stats.at[possPlayer["id"].item(),"DREB",] += 1
                                                possTeam = t1
                                                offense = t1
                                                defense = t2
                                                offense_df = t1onCourt
                                                defense_df = t2onCourt
                                                courtPos = (random.randint(2,4) * -1,random.randint(2,4))

                                            currShotClock = shotClock
                                            if currTime <= shotClock:
                                                currShotClock = currTime
                                            crossed_midcourt = False
                                            print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " grabs the defensive rebound for " + possTeam)
                                            defendedPlayerId = None
                                            currentDefender = None
                                            previousDefender = None

                                    else:
                                        if offense == t1:
                                            possTeam = t2
                                            offense = t2
                                            defense = t1
                                            offense_df = t2onCourt
                                            defense_df = t1onCourt
                                            courtPos = (4,3)
                                            possPlayer = random.choice(list(t2onCourt.values()))
                                        else:
                                            possTeam = t1
                                            offense = t1
                                            defense = t2
                                            offense_df = t1onCourt
                                            defense_df = t2onCourt
                                            courtPos = (-4,3)
                                            possPlayer = random.choice(list(t1onCourt.values()))

                                        crossed_midcourt = False
                                        currShotClock = shotClock
                                        if currTime <= shotClock:
                                            currShotClock = currTime
                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None
                                        print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out for " + possTeam)
                                        finalHeavePending = True

                                    print(footerPos)
                                    printMomentumMeter()
                            else:
                                assistPlayer = None
                                assistMovementCount = 0
                                offensivePlayerFouledOut = False
                                offensivePlayerFoulProtected = False
                                offensivePlayerStatId = possPlayer["id"].item()
                                offensivePlayerId = int(possPlayer["player_id"])

                                if offense == t1:
                                    t1stats.at[offensivePlayerStatId,"Foul",] += 1
                                    t1stats.at[offensivePlayerStatId,"TO",] += 1
                                    if period == 1:
                                        t1FirstHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = t1FirstHalfTeamFouls
                                    else:
                                        t1SecondHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = t1SecondHalfTeamFouls

                                    offensivePlayerFoulTotal = int(t1stats.at[offensivePlayerStatId,"Foul"])
                                    if offensivePlayerFoulTotal >= foulOutLimit and offensivePlayerId not in t1FouledOutPlayerIds:
                                        t1FouledOutPlayerIds.add(offensivePlayerId)
                                        offensivePlayerFouledOut = True
                                    offensivePlayerFoulProtected = registerFoulProtection(1,offensivePlayerStatId,offensivePlayerId,f"{possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']}")
                                else:
                                    t2stats.at[offensivePlayerStatId,"Foul",] += 1
                                    t2stats.at[offensivePlayerStatId,"TO",] += 1
                                    if period == 1:
                                        t2FirstHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = t2FirstHalfTeamFouls
                                    else:
                                        t2SecondHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = t2SecondHalfTeamFouls

                                    offensivePlayerFoulTotal = int(t2stats.at[offensivePlayerStatId,"Foul"])
                                    if offensivePlayerFoulTotal >= foulOutLimit and offensivePlayerId not in t2FouledOutPlayerIds:
                                        t2FouledOutPlayerIds.add(offensivePlayerId)
                                        offensivePlayerFouledOut = True
                                    offensivePlayerFoulProtected = registerFoulProtection(2,offensivePlayerStatId,offensivePlayerId,f"{possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']}")

                                print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                                print(f"OFFENSIVE FOUL! {possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} is called for a charge drawn by {defender['position']} {defender['first_name']} {defender['last_name']}!")
                                print(f"Offensive team fouls this half: {offensiveHalfTeamFouls}")

                                if offensivePlayerFouledOut:
                                    print(f"{possPlayer['position']} {possPlayer['first_name']} {possPlayer['last_name']} has fouled out with {offensivePlayerFoulTotal} fouls!")

                                offensiveFoulMediaTimeoutTaken = checkTimeoutStoppage(defense,True)

                                if (offensivePlayerFouledOut or offensivePlayerFoulProtected) and not offensiveFoulMediaTimeoutTaken:
                                    t1onCourt,t2onCourt,lineupParameters = pullSubs(False)
                                    substitutionReason = "foul-out" if offensivePlayerFouledOut else "foul protection"
                                    print(t1 + " Subs after " + substitutionReason + ":")
                                    for lineupPlayer in t1onCourt.values():
                                        print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])
                                    print(t2 + " Subs after " + substitutionReason + ":")
                                    for lineupPlayer in t2onCourt.values():
                                        print(lineupPlayer["position"] + " " + lineupPlayer["first_name"] + " " + lineupPlayer["last_name"])

                                if offense == t1:
                                    possTeam = t2
                                    offense = t2
                                    defense = t1
                                    offense_df = t2onCourt
                                    defense_df = t1onCourt
                                    courtPos = (4,3)
                                    possPlayer = random.choice(list(t2onCourt.values()))
                                else:
                                    possTeam = t1
                                    offense = t1
                                    defense = t2
                                    offense_df = t1onCourt
                                    defense_df = t2onCourt
                                    courtPos = (-4,3)
                                    possPlayer = random.choice(list(t1onCourt.values()))

                                crossed_midcourt = False
                                currShotClock = shotClock
                                if currTime <= shotClock:
                                    currShotClock = currTime
                                assistPlayer = None
                                defendedPlayerId = None
                                currentDefender = None
                                previousDefender = None
                                print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out for " + possTeam + ".")
                                finalHeavePending = True
                                print(footerPos)
                                printMomentumMeter()
                        else:
                            print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                            print(possPlayer["position"] + " " + possPlayer ["first_name"] + " " + possPlayer["last_name"] + " is trapped and cannot move.")
                            print(footerPos)
                            printMomentumMeter()


                    elif action == "pass":
                        formationDestinationWeights = t1FormationDestinationWeights if offense == t1 else t2FormationDestinationWeights
                        activeDestinationWeights,activeLineupPreferences = getActiveDestinationWeights(offense_df,formationDestinationWeights)
                        targetPos = choose_weighted_pass_target(
                            team_side,
                            courtPos,
                            crossed_midcourt,
                            activeDestinationWeights,
                        )

                        if targetPos is not None:
                            offenseStats = t1stats if offense == t1 else t2stats
                            defenseStats = t2stats if offense == t1 else t1stats

                            possPlayerMinutes = float(offenseStats.at[possPlayer["id"].item(),"MP"]) / 60
                            defenderMinutes = float(defenseStats.at[defender["id"].item(),"MP"]) / 60
                            possPlayerRecoveryMinutes = getPlayerRecoveryMinutes(possPlayer)
                            defenderRecoveryMinutes = getPlayerRecoveryMinutes(defender)
                            possPlayerFatigueMinutes = max(0.0,possPlayerMinutes - possPlayerRecoveryMinutes)
                            defenderFatigueMinutes = max(0.0,defenderMinutes - defenderRecoveryMinutes)

                            (passOffense,basePassOffense,offensiveStaminaCapacity,possPlayerMinutes,offensiveStaminaUsageRatio,offensiveFatiguePenalty,offensiveStaminaModifier,) = get_stamina_adjusted_rating(possPlayer,"ballwork",possPlayerMinutes,possPlayerRecoveryMinutes)
                            passOffenseType = "ballwork"
                            staminaAdjustedPassOffense = passOffense
                            (passOffense,passMomentumStrength,passMomentumBonus,passMomentumModifier,) = getMomentumAdjustedRating(staminaAdjustedPassOffense,offense)
                            (_,_,defenderStaminaCapacity,defenderMinutes,defenderStaminaUsageRatio,defenderFatiguePenalty,defenderStaminaModifier,) = get_stamina_adjusted_rating(defender,"perimeter_defense",defenderMinutes,defenderRecoveryMinutes)

                            basePassDefense,passDefenseType = get_movement_defense(defender,courtPos)
                            passDefense,passDefenseType = get_movement_defense(defender,courtPos,defenderStaminaModifier)

                            distanceDeflectionChance = (
                                get_pass_turnover_chance(
                                    courtPos,
                                    targetPos,
                                )
                            )
                            passDeflectionChance = (
                                get_pass_deflection_chance(
                                    courtPos,
                                    targetPos,
                                    passOffense,
                                    passDefense,
                                )
                            )
                            passDeflectionChance = max(passDeflectionMinimum,min(passDeflectionMaximum,passDeflectionChance + doubleTeamPassDeflectionAdjustment))
                            passRoll = random.random()
                            passDeflected = (
                                    passRoll < passDeflectionChance
                            )

                            print(f"Pass offense: {passOffense:.4f} [{passOffenseType}; base {basePassOffense:.2f}; stamina adjusted {staminaAdjustedPassOffense:.4f}; MP {possPlayerMinutes:.2f}; recovery {possPlayerRecoveryMinutes:.2f}; fatigue load {possPlayerFatigueMinutes:.2f}/{offensiveStaminaCapacity:.2f}; stamina modifier {offensiveStaminaModifier:.3f}; momentum {passMomentumStrength:.0%}; momentum bonus {passMomentumBonus:.2%}; momentum modifier {passMomentumModifier:.3f}] | Pass defense: {passDefense:.4f} [{passDefenseType}; base {basePassDefense:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Distance chance: {distanceDeflectionChance:.2%} | Double-team role: {doubleTeamRole} {doubleTeamPassDeflectionAdjustment:+.2%} | Final deflection chance: {passDeflectionChance:.2%} | Roll: {passRoll:.4f} | {'DEFLECTED' if passDeflected else 'CLEAN'} toward {format_court_pos(targetPos)}")

                            if passDeflected:
                                looseRand = random.random()
                                if possTeam == t1:
                                    looseBallCO = lineupParameters["t1LooseBall"]
                                else:
                                    looseBallCO = lineupParameters["t2LooseBall"]
                                if looseRand < looseBallCO:
                                    pickupPlayer = random.choice(list(offense_df.values()))
                                    print("Pass from " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " toward " + format_court_pos(targetPos) + " is deflected! His teammate " + pickupPlayer["position"] + " " + pickupPlayer["first_name"] + " " + pickupPlayer["last_name"] + " recovers it.")
                                    print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                                    print(footerPos)
                                    printMomentumMeter()
                                    possPlayer = pickupPlayer
                                    assistPlayer = None
                                else:
                                    pickupPlayer = random.choice(list(defense_df.values()))
                                    print("Pass from " + possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " toward " + format_court_pos(targetPos) + " is deflected! It's recovered by " + pickupPlayer["position"] + " " + pickupPlayer["first_name"] + " " + pickupPlayer["last_name"] + " for " + defense)
                                    currShotClock = shotClock
                                    if currTime <= shotClock:
                                        currShotClock = currTime
                                    crossed_midcourt = False
                                    if possTeam == t1:
                                        t1stats.at[possPlayer['id'].item(), 'TO'] += 1
                                        t2stats.at[pickupPlayer['id'].item(), 'Stl'] += 1
                                        possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = t2onCourt
                                        defense_df = t1onCourt
                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None
                                    else:
                                        t2stats.at[possPlayer['id'].item(), 'TO'] += 1
                                        t1stats.at[pickupPlayer['id'].item(), 'Stl'] += 1
                                        possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = t1onCourt
                                        defense_df = t2onCourt
                                        defendedPlayerId = None
                                        currentDefender = None
                                        previousDefender = None
                                    possPlayer = pickupPlayer
                                    pickupPlayer = ""
                                    assistPlayer = None

                            else:
                                assistPlayer = possPlayer
                                assistMovementCount = 0
                                eligiblePassReceivers = [player for player in offense_df.values() if int(player["id"]) != int(possPlayer["id"])]
                                passTargetPreferenceZone = getPreferenceZone(get_shot_zone(targetPos))
                                if passTargetPreferenceZone is not None:
                                    passTargetPreferenceColumn = {"inside":"inside_preference","midrange":"midrange_preference","three":"three_preference"}[passTargetPreferenceZone]
                                    passReceiverWeights = [max(passReceiverPreferenceMinimumWeight,min(passReceiverPreferenceMaximumWeight,1.0 + ((float(player[passTargetPreferenceColumn]) - activeLineupPreferences[passTargetPreferenceZone]) * passReceiverPreferenceWeightPerProportionPoint))) for player in eligiblePassReceivers]
                                    passReceiverIndex = random.choices(range(len(eligiblePassReceivers)),weights=passReceiverWeights,k=1)[0]
                                    passReceive = eligiblePassReceivers[passReceiverIndex]
                                    print(f"Pass receiver preference: {passTargetPreferenceZone} | Selected: {passReceive['first_name']} {passReceive['last_name']} {float(passReceive[passTargetPreferenceColumn]):.1f}% | Active lineup: {activeLineupPreferences[passTargetPreferenceZone]:.1f}% | Selection weight: {passReceiverWeights[passReceiverIndex]:.3f}")
                                else:
                                    passReceive = random.choice(eligiblePassReceivers)
                                courtPos = targetPos
                                crossed_midcourt = update_crossed_midcourt(team_side, courtPos, crossed_midcourt)
                                print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                                print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " passes the ball to " + passReceive["position"] + " " + passReceive["first_name"] + " " + passReceive["last_name"] + ".")
                                print(footerPos)
                                printMomentumMeter()
                                possPlayer = passReceive
                                passReceive = ""

                        else:
                            assistPlayer = None
                            print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                            print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " has no legal passing lane.")
                            print(footerPos)
                            printMomentumMeter()

                    elif action == "turnover":
                        assistPlayer = None
                        turnoverTeam = possTeam
                        if turnoverTeam == t1:
                            t1stats.at[possPlayer["id"].item(),"TO"] += 1
                        else:
                            t2stats.at[possPlayer["id"].item(),"TO"] += 1

                        print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                        print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " loses the ball out of bounds.")

                        mediaTimeoutTaken = checkTimeoutStoppage(defense,True)
                        if not mediaTimeoutTaken:
                            t1onCourt,t2onCourt,lineupParameters = pullSubs(False)
                            print(t1 + " Subs:")
                            for i in list(t1onCourt.values()):
                                print(i["position"] + " " + i["first_name"] + " " + i["last_name"])
                            print(t2 + " Subs:")
                            for i in list(t2onCourt.values()):
                                print(i["position"] + " " + i["first_name"] + " " + i["last_name"])

                        if turnoverTeam == t1:
                            offense_df = t2onCourt
                            defense_df = t1onCourt
                        else:
                            offense_df = t1onCourt
                            defense_df = t2onCourt

                        toTakeout = random.choice(list(offense_df.values()))
                        print(toTakeout["position"] + " " + toTakeout["first_name"] + " " + toTakeout["last_name"] + " will take the ball out for " + defense + ".")
                        finalHeavePending = True
                        print(footerPos)
                        printMomentumMeter()
                        currShotClock = shotClock
                        if currTime <= shotClock:
                            currShotClock = currTime
                        possPlayer = toTakeout
                        defendedPlayerId = None
                        currentDefender = None
                        previousDefender = None

                        if turnoverTeam == t1:
                            possTeam = t2
                            offense = t2
                            defense = t1
                            if crossed_midcourt == False:
                                courtPos = (-2,1)
                            else:
                                courtPos = (2,1)
                        else:
                            possTeam = t1
                            offense = t1
                            defense = t2
                            if crossed_midcourt == False:
                                courtPos = (2,1)
                            else:
                                courtPos = (-2,1)

                    elif action == "steal":
                        assistPlayer = None
                        stealPlayer = random.choice(list(defense_df.values()))
                        print((str(period) + pInd if period <= periodPerGame else "OT"+str(period-periodPerGame))+ ": "+game_clock_text+ " / Shot Clock: :"+ shot_clock_text+ " ("+ possTeam+ ")")
                        print(stealPlayer["position"] + " " + stealPlayer["first_name"] + " " + stealPlayer["last_name"] + " picks the ball away for " + defense + "!")
                        adjustMomentum(defense,momentumStealSwing,"steal")
                        print(footerPos)
                        printMomentumMeter()
                        if possTeam == t1:
                            t1stats.at[possPlayer['id'].item(), 'TO'] += 1
                            t2stats.at[stealPlayer['id'].item(), 'Stl'] += 1
                            possTeam = t2
                            offense = t2
                            defense = t1
                            offense_df = t2onCourt
                            defense_df = t1onCourt
                            defendedPlayerId = None
                            currentDefender = None
                            previousDefender = None
                        else:
                            t2stats.at[possPlayer['id'].item(), 'TO'] += 1
                            t1stats.at[stealPlayer['id'].item(), 'Stl'] += 1
                            possTeam = t1
                            offense = t1
                            defense = t2
                            offense_df = t1onCourt
                            defense_df = t2onCourt
                            defendedPlayerId = None
                            currentDefender = None
                            previousDefender = None
                        possPlayer = stealPlayer
                        stealPlayer = ""
                        currShotClock = shotClock
                        if currTime <= shotClock:
                            currShotClock = currTime
                        crossed_midcourt = False

        if currTime <= 0 and gameOn == True:
            periodOn = False
            assistPlayer = None
            if period < periodPerGame:
                print("End of "+("Half " if league == "CBB" else "Quarter ")+str(period)+".\n"+t1+": "+str(t1pts)+" / "+t2+": "+str(t2pts))
                period += 1
                lastCountedPossessionTeam = None
                if (league == "CBB" and period == 2) or (league != "CBB" and period == 3):
                    t1FoulProtectionBench.clear()
                    t2FoulProtectionBench.clear()
                    t1PlayerHalfFouls.clear()
                    t2PlayerHalfFouls.clear()
                    print("Halftime: all foul-protection restrictions have been cleared.")
                if league == "CBB":
                    applyFatigueRecovery(halftimeRecoveryMinutes,"Halftime breather")
                    dampenMomentum(momentumHalftimeRetention,"halftime")
                elif period == 3:
                    applyFatigueRecovery(halftimeRecoveryMinutes,"Halftime breather")
                    dampenMomentum(momentumHalftimeRetention,"halftime")
                else:
                    applyFatigueRecovery(quarterBreakRecoveryMinutes,"Quarter-break breather")
                    dampenMomentum(momentumQuarterBreakRetention,"quarter break")
                if league == "CBB" and period == 2:
                    t1onCourt, t2onCourt, lineupParameters = pullSubs(True)
                    print(t1 + " Subs:")
                    for i in list(t1onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                    print(t2 + " Subs:")
                    for i in list(t2onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                elif league != "CBB" and period == 3:
                    print(t1 + " Subs:")
                    t1onCourt, t2onCourt, lineupParameters = pullSubs(True)
                    for i in list(t1onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                    print(t2 + " Subs:")
                    for i in list(t2onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                else:
                    t1onCourt, t2onCourt, lineupParameters = pullSubs(False)
                    print(t1 + " Subs:")
                    for i in list(t1onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                    print(t2 + " Subs:")
                    for i in list(t2onCourt.values()):
                        print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                currShotClock = shotClock
                currTime = qtrTime
                crossed_midcourt = False
                if possTeam == t1:
                    toTakeout = random.choice(list(t1onCourt.values()))
                    possPlayer = toTakeout
                    toTakeout = ""
                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out to begin the " + ("half " if league == "CBB" else "quarter ") + " for " + possTeam + ".")
                    finalHeavePending = True
                    courtPos = (4, 3)
                elif possTeam == t2:
                    toTakeout = random.choice(list(t2onCourt.values()))
                    possPlayer = toTakeout
                    toTakeout = ""
                    print(possPlayer["position"] + " " + possPlayer["first_name"] + " " + possPlayer["last_name"] + " takes the ball out to begin the " + ("half " if league == "CBB" else "quarter ") + " for " + possTeam + ".")
                    finalHeavePending = True
                    courtPos = (-4, 3)
                periodOn = True
            elif period >= periodPerGame and t1pts == t2pts:
                print("We're headed to overtime!")
                period += 1
                lastCountedPossessionTeam = None
                overtimeTimeoutAddition = 1 if league == "CBB" else 2
                teamTimeoutsRemaining[t1] += overtimeTimeoutAddition
                teamTimeoutsRemaining[t2] += overtimeTimeoutAddition
                print(f"Overtime timeout allocation: {t1} and {t2} each receive {overtimeTimeoutAddition} additional timeout{'s' if overtimeTimeoutAddition != 1 else ''}.")
                applyFatigueRecovery(overtimeBreakRecoveryMinutes,"Overtime breather")
                dampenMomentum(momentumOvertimeBreakRetention,"overtime break")
                currShotClock = shotClock
                currTime = otQtrTime
                t1onCourt, t2onCourt, lineupParameters = pullSubs(True)
                print(t1 + " Subs:")
                for i in list(t1onCourt.values()):
                    print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                print(t2 + " Subs:")
                for i in list(t2onCourt.values()):
                    print(i['position'] + " " + i['first_name'] + " " + i['last_name'])
                crossed_midcourt = False
                courtPos = (0,3)
                possTeam = "OT_TIPOFF"
                periodOn = True
            else:
                print("End of the game.")
                gameOn = False

    if gameOn == False:
        #print("    " + t1 + "  |    " + t2)
        #print(pInd + "1: " + str(t1q1pts) + "    |    " + str(t2q1pts))
        #print(pInd + "2: " + str(t1q2pts) + "    |    " + str(t2q2pts))
        #if league != "CBB":
            #print("Q3: " + str(t1q3pts) + "    |    " + str(t2q3pts))
            #print("Q4: " + str(t1q4pts) + "    |    " + str(t2q4pts))
        #if (period - 1) > periodPerGame:
            #print("OT: " + str(t1qotpts) + "    |    " + str(t2qotpts))
        #print("F:  " + str(t1pts) + "   |    " + str(t2pts))
        #print(" ")
        #print("2Pt: " + str(t12m) + "/" + str(t12a) + " | " + str(t22m) + "/" + str(t22a))
        #print("3Pt: " + str(t13m) + "/" + str(t13a) + " | " + str(t23m) + "/" + str(t23a))

        t1stats["MP"] = (t1stats["MP"] / 60).round(2)
        t1stats['Pts'] = (t1stats['FT Shot Made']*1) + (t1stats['Ins Shot Made']*2) + (t1stats['Mid Shot Made']*2) + (t1stats['3PT Shot Made']*3)
        t1stats['TREB'] = (t1stats['DREB'] + t1stats['OREB'])
        try:
            t1stats['Ins Shot %'] = (((t1stats['Ins Shot Made'] / t1stats['Ins Shot Att'])).round(4))*100
        except ZeroDivisionError:
            t1stats['Ins Shot %'] = 0
        try:
            t1stats['Mid Shot %'] = (((t1stats['Mid Shot Made'] / t1stats['Mid Shot Att'])).round(4))*100
        except ZeroDivisionError:
            t1stats['Mid Shot %'] = 0
        try:
            t1stats['3PT Shot %'] = (((t1stats['3PT Shot Made'] / t1stats['3PT Shot Att'])).round(4))*100
        except ZeroDivisionError:
            t1stats['3PT Shot %'] = 0
        try:
            t1stats['FT Shot %'] = (((t1stats['FT Shot Made'] / t1stats['FT Shot Att'])).round(4))*100
        except ZeroDivisionError:
            t1stats['FT Shot %'] = 0

        try:
            t1teamstats['Ins Shot %'] = (((t1stats['Ins Shot Made'].sum() / t1stats['Ins Shot Att'].sum())).round(4))*100
        except ZeroDivisionError:
            t1teamstats['Ins Shot %'] = 0
        try:
            t1teamstats['Mid Shot %'] = (((t1stats['Mid Shot Made'].sum() / t1stats['Mid Shot Att'].sum())).round(4))*100
        except ZeroDivisionError:
            t1teamstats['Mid Shot %'] = 0
        try:
            t1teamstats['3PT Shot %'] = (((t1stats['3PT Shot Made'].sum() / t1stats['3PT Shot Att'].sum())).round(4))*100
        except ZeroDivisionError:
            t1teamstats['3PT Shot %'] = 0
        try:
            t1teamstats['FT Shot %'] = (((t1stats['FT Shot Made'].sum() / t1stats['FT Shot Att'].sum())).round(4))*100
        except ZeroDivisionError:
            t1teamstats['FT Shot %'] = 0
        t1teamstats['Ins Shot Att'] = t1stats['Ins Shot Att'].sum()
        t1teamstats['Ins Shot Made'] = t1stats['Ins Shot Made'].sum()
        t1teamstats['Mid Shot Att'] = t1stats['Mid Shot Att'].sum()
        t1teamstats['Mid Shot Made'] = t1stats['Mid Shot Made'].sum()
        t1teamstats['3PT Shot Att'] = t1stats['3PT Shot Att'].sum()
        t1teamstats['3PT Shot Made'] = t1stats['3PT Shot Made'].sum()
        t1teamstats['FT Shot Att'] = t1stats['FT Shot Att'].sum()
        t1teamstats['FT Shot Made'] = t1stats['FT Shot Made'].sum()
        t1teamstats['TREB'] = (t1stats['DREB'].sum() + t1stats['OREB'].sum())
        t1teamstats['OREB'] = t1stats['OREB'].sum()
        t1teamstats['DREB'] = t1stats['DREB'].sum()
        t1teamstats['Stl'] = t1stats['Stl'].sum()
        t1teamstats['Blk'] = t1stats['Blk'].sum()
        t1teamstats['TO'] = t1stats['TO'].sum()
        t1teamstats['Foul'] = t1stats['Foul'].sum()
        t1teamstats['Assist'] = t1stats['Assist'].sum()
        t1teamstats['Poss'] = teamPossessions[t1]
        t1teamstats['TOP'] = f"{int(teamPossessionTime[t1] // 60):02d}:{teamPossessionTime[t1] % 60:04.1f}"
        t1teamstats['Pts'] = (t1stats['FT Shot Made'].sum()*1) + (t1stats['Ins Shot Made'].sum()*2) + (t1stats['Mid Shot Made'].sum()*2) + (t1stats['3PT Shot Made'].sum()*3)

        t2stats["MP"] = (t2stats["MP"] / 60).round(2)
        t2stats['Pts'] = (t2stats['FT Shot Made']*1) + (t2stats['Ins Shot Made']*2) + (t2stats['Mid Shot Made']*2) + (t2stats['3PT Shot Made']*3)
        t2stats['TREB'] = (t2stats['DREB'] + t2stats['OREB'])
        try:
            t2stats['Ins Shot %'] = (((t2stats['Ins Shot Made'] / t2stats['Ins Shot Att'])).round(4)*100)
        except ZeroDivisionError:
            t2stats['Ins Shot %'] = 0
        try:
            t2stats['Mid Shot %'] = (((t2stats['Mid Shot Made'] / t2stats['Mid Shot Att'])).round(4)*100)
        except ZeroDivisionError:
            t2stats['Mid Shot %'] = 0
        try:
            t2stats['3PT Shot %'] = (((t2stats['3PT Shot Made'] / t2stats['3PT Shot Att'])).round(4)*100)
        except ZeroDivisionError:
            t2stats['3PT Shot %'] = 0
        try:
            t2stats['FT Shot %'] = (((t2stats['FT Shot Made'] / t2stats['FT Shot Att'])).round(4)*100)
        except ZeroDivisionError:
            t2stats['FT Shot %'] = 0

        try:
            t2teamstats['Ins Shot %'] = (((t2stats['Ins Shot Made'].sum() / t2stats['Ins Shot Att'].sum())).round(4)*100)
        except ZeroDivisionError:
            t2teamstats['Ins Shot %'] = 0
        try:
            t2teamstats['Mid Shot %'] = (((t2stats['Mid Shot Made'].sum() / t2stats['Mid Shot Att'].sum())).round(4)*100)
        except ZeroDivisionError:
            t2teamstats['Mid Shot %'] = 0
        try:
            t2teamstats['3PT Shot %'] = (((t2stats['3PT Shot Made'].sum() / t2stats['3PT Shot Att'].sum())).round(4)*100)
        except ZeroDivisionError:
            t2teamstats['3PT Shot %'] = 0
        try:
            t2teamstats['FT Shot %'] = (((t2stats['FT Shot Made'].sum() / t2stats['FT Shot Att'].sum())).round(4)*100)
        except ZeroDivisionError:
            t2teamstats['FT Shot %'] = 0
        t2teamstats['Ins Shot Att'] = t2stats['Ins Shot Att'].sum()
        t2teamstats['Ins Shot Made'] = t2stats['Ins Shot Made'].sum()
        t2teamstats['Mid Shot Att'] = t2stats['Mid Shot Att'].sum()
        t2teamstats['Mid Shot Made'] = t2stats['Mid Shot Made'].sum()
        t2teamstats['3PT Shot Att'] = t2stats['3PT Shot Att'].sum()
        t2teamstats['3PT Shot Made'] = t2stats['3PT Shot Made'].sum()
        t2teamstats['FT Shot Att'] = t2stats['FT Shot Att'].sum()
        t2teamstats['FT Shot Made'] = t2stats['FT Shot Made'].sum()
        t2teamstats['TREB'] = (t2stats['DREB'].sum() + t2stats['OREB'].sum())
        t2teamstats['OREB'] = t2stats['OREB'].sum()
        t2teamstats['DREB'] = t2stats['DREB'].sum()
        t2teamstats['Stl'] = t2stats['Stl'].sum()
        t2teamstats['Blk'] = t2stats['Blk'].sum()
        t2teamstats['TO'] = t2stats['TO'].sum()
        t2teamstats['Foul'] = t2stats['Foul'].sum()
        t2teamstats['Assist'] = t2stats['Assist'].sum()
        t2teamstats['Poss'] = teamPossessions[t2]
        t2teamstats['TOP'] = f"{int(teamPossessionTime[t2] // 60):02d}:{teamPossessionTime[t2] % 60:04.1f}"
        t2teamstats['Pts'] = (t2stats['FT Shot Made'].sum()*1) + (t2stats['Ins Shot Made'].sum()*2) + (t2stats['Mid Shot Made'].sum()*2) + (t2stats['3PT Shot Made'].sum()*3)

        t1teamscore['P1'] = t1q1pts
        t1teamscore['P2'] = t1q2pts
        t1teamscore['P3'] = t1q3pts
        t1teamscore['P4'] = t1q4pts
        t1teamscore['OT'] = t1qotpts
        t1teamscore['F'] = t1q1pts + t1q2pts + t1q3pts + t1q4pts + t1qotpts

        t2teamscore['P1'] = t2q1pts
        t2teamscore['P2'] = t2q2pts
        t2teamscore['P3'] = t2q3pts
        t2teamscore['P4'] = t2q4pts
        t2teamscore['OT'] = t2qotpts
        t2teamscore['F'] = t2q1pts + t2q2pts + t2q3pts + t2q4pts + t2qotpts

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)
        teamscore = pd.concat([t1teamscore, t2teamscore], axis=0)
        teamstats = pd.concat([t1teamstats, t2teamstats], axis=0)
        print(teamscore)
        print(teamstats)
        print(t1stats[t1stats["MP"] > 0.00])
        print(t2stats[t2stats["MP"] > 0.00])
        return teamscore,teamstats,t1stats,t2stats
