import csv
import random
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import math

from baseprobabilities import *
from gamestate import *

from bbdef import *
from courtDef import *


def rungame(match, gamenum=1):
    gs = GameState(match, gamenum)
    t1 = gs.t1
    t2 = gs.t2

    _FOOTER = {
        (
            -4,
            1,
        ): "|x        |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -3,
            1,
        ): "|  x      |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -2,
            1,
        ): "|    x    |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -1,
            1,
        ): "|      x  |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            0,
            1,
        ): "|         x         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            1,
            1,
        ): "|         |  x      |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            2,
            1,
        ): "|         |    x    |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            3,
            1,
        ): "|         |      x  |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            4,
            1,
        ): "|         |        x|\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -4,
            2,
        ): "|         |         |\n|x        |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -3,
            2,
        ): "|         |         |\n|  x      |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -2,
            2,
        ): "|         |         |\n|    x    |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -1,
            2,
        ): "|         |         |\n|      x  |         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            0,
            2,
        ): "|         |         |\n|         x         |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            1,
            2,
        ): "|         |         |\n|         |  x      |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            2,
            2,
        ): "|         |         |\n|         |    x    |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            3,
            2,
        ): "|         |         |\n|         |      x  |\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            4,
            2,
        ): "|         |         |\n|         |        x|\n|-O       |       O-|\n|         |         |\n|         |         |",
        (
            -4,
            3,
        ): "|         |         |\n|         |         |\n|-x       |       O-|\n|         |         |\n|         |         |",
        (
            -3,
            3,
        ): "|         |         |\n|         |         |\n|-Ox      |       O-|\n|         |         |\n|         |         |",
        (
            -2,
            3,
        ): "|         |         |\n|         |         |\n|-O  x    |       O-|\n|         |         |\n|         |         |",
        (
            -1,
            3,
        ): "|         |         |\n|         |         |\n|-O    x  |       O-|\n|         |         |\n|         |         |",
        (
            0,
            3,
        ): "|         |         |\n|         |         |\n|-O       x       O-|\n|         |         |\n|         |         |",
        (
            1,
            3,
        ): "|         |         |\n|         |         |\n|-O       |  x    O-|\n|         |         |\n|         |         |",
        (
            2,
            3,
        ): "|         |         |\n|         |         |\n|-O       |    x  O-|\n|         |         |\n|         |         |",
        (
            3,
            3,
        ): "|         |         |\n|         |         |\n|-O       |      xO-|\n|         |         |\n|         |         |",
        (
            4,
            3,
        ): "|         |         |\n|         |         |\n|-O       |       x-|\n|         |         |\n|         |         |",
        (
            -4,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|x        |         |\n|         |         |",
        (
            -3,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|  x      |         |\n|         |         |",
        (
            -2,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|    x    |         |\n|         |         |",
        (
            -1,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|      x  |         |\n|         |         |",
        (
            0,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         x         |\n|         |         |",
        (
            1,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |  x      |\n|         |         |",
        (
            2,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |    x    |\n|         |         |",
        (
            3,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |      x  |\n|         |         |",
        (
            4,
            4,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |        x|\n|         |         |",
        (
            -4,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|x        |         |",
        (
            -3,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|  x      |         |",
        (
            -2,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|    x    |         |",
        (
            -1,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|      x  |         |",
        (
            0,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         x         |",
        (
            1,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |  x      |",
        (
            2,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |    x    |",
        (
            3,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |      x  |",
        (
            4,
            5,
        ): "|         |         |\n|         |         |\n|-O       |       O-|\n|         |         |\n|         |        x|",
    }

    while gs.gameOn and gs.periodOn:
        tipoffJustOccurred = False
        footerPos = _FOOTER.get(gs.courtPos, "TIPOFF")
        periodLabel = (
            str(gs.period) + gs.pInd if gs.period <= gs.periodPerGame else "OT" + str(gs.period - gs.periodPerGame)
        )

        if gs.possTeam == "TIPOFF":
            print("Game Starting\nT1 (Home): " + t1 + "\nT2 (Away): " + t2)
            print(
                f"{t1} Pace: {gs.t1Pace} | Available stamina modifier: {gs.t1PaceStaminaModifier:.0%} | Expected action-time modifier: {gs.t1ExpectedActionTimeModifier:.2f}"
            )
            print(
                f"{t2} Pace: {gs.t2Pace} | Available stamina modifier: {gs.t2PaceStaminaModifier:.0%} | Expected action-time modifier: {gs.t2ExpectedActionTimeModifier:.2f}"
            )
            print(
                f"{t1} Formations: {gs.t1OffensiveFormation} offense vs {gs.t2DefensiveFormation} defense | Destination weights: inside {gs.t1FormationDestinationWeights['inside']:.3f}, midrange {gs.t1FormationDestinationWeights['midrange']:.3f}, three {gs.t1FormationDestinationWeights['three']:.3f} | OREB adjustment: {gs.t1FormationOffensiveReboundAdjustment:+.2%} | Opponent focus: {gs.t2FocusPlayerId or 'none'}"
            )
            print(
                f"{t2} Formations: {gs.t2OffensiveFormation} offense vs {gs.t1DefensiveFormation} defense | Destination weights: inside {gs.t2FormationDestinationWeights['inside']:.3f}, midrange {gs.t2FormationDestinationWeights['midrange']:.3f}, three {gs.t2FormationDestinationWeights['three']:.3f} | OREB adjustment: {gs.t2FormationOffensiveReboundAdjustment:+.2%} | Opponent focus: {gs.t1FocusPlayerId or 'none'}"
            )
            print(t1 + " Starters:")
            for p in gs.t1onCourt.values():
                print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
            print(t2 + " Starters:")
            for p in gs.t2onCourt.values():
                print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
            tipRoll = random.random()
            if tipRoll < gs.t1TipChance:
                gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                gs.possTeam = t1
                offense = t1
                defense = t2
                offense_df = gs.t1onCourt
                defense_df = gs.t2onCourt
                gs.addPlayingTime(1)
                gs.currTime -= 1
                print(
                    str(gs.t1onCourt["c1"]["position"])
                    + " "
                    + str(gs.t1onCourt["c1"]["first_name"])
                    + " "
                    + str(gs.t1onCourt["c1"]["last_name"])
                    + " wins the tipoff for "
                    + t1
                    + ". "
                    + gs.possPlayer["position"]
                    + " "
                    + gs.possPlayer["first_name"]
                    + " "
                    + gs.possPlayer["last_name"]
                    + " takes control of the ball."
                )
            else:
                gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                gs.possTeam = t2
                offense = t2
                defense = t1
                offense_df = gs.t2onCourt
                defense_df = gs.t1onCourt
                gs.addPlayingTime(1)
                gs.currTime -= 1
                print(
                    str(gs.t2onCourt["c1"]["position"])
                    + " "
                    + str(gs.t2onCourt["c1"]["first_name"])
                    + " "
                    + str(gs.t2onCourt["c1"]["last_name"])
                    + " wins the tipoff for "
                    + t2
                    + ". "
                    + gs.possPlayer["position"]
                    + " "
                    + gs.possPlayer["first_name"]
                    + " "
                    + gs.possPlayer["last_name"]
                    + " takes control of the ball."
                )
            gs.teamPossessionTime[gs.possTeam] += 1.0
            tipoffJustOccurred = True

        if gs.possTeam == "OT_TIPOFF":
            tipRoll = random.random()
            if tipRoll < gs.t1TipChance:
                gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                gs.possTeam = t1
                offense = t1
                defense = t2
                offense_df = gs.t1onCourt
                defense_df = gs.t2onCourt
                gs.addPlayingTime(1)
                gs.currTime -= 1
                print(
                    str(gs.t1onCourt["c1"]["position"])
                    + " "
                    + str(gs.t1onCourt["c1"]["first_name"])
                    + " "
                    + str(gs.t1onCourt["c1"]["last_name"])
                    + " wins the tipoff for "
                    + t1
                    + ". "
                    + gs.possPlayer["position"]
                    + " "
                    + gs.possPlayer["first_name"]
                    + " "
                    + gs.possPlayer["last_name"]
                    + " takes control of the ball."
                )
            else:
                gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                gs.possTeam = t2
                offense = t2
                defense = t1
                offense_df = gs.t2onCourt
                defense_df = gs.t1onCourt
                gs.addPlayingTime(1)
                gs.currTime -= 1
                print(
                    str(gs.t2onCourt["c1"]["position"])
                    + " "
                    + str(gs.t2onCourt["c1"]["first_name"])
                    + " "
                    + str(gs.t2onCourt["c1"]["last_name"])
                    + " wins the tipoff for "
                    + t2
                    + ". "
                    + gs.possPlayer["position"]
                    + " "
                    + gs.possPlayer["first_name"]
                    + " "
                    + gs.possPlayer["last_name"]
                    + " takes control of the ball."
                )
            gs.teamPossessionTime[gs.possTeam] += 1.0
            tipoffJustOccurred = True

        if gs.possTeam == t1 or gs.possTeam == t2:
            if gs.possTeam != gs.lastCountedPossessionTeam:
                gs.teamPossessions[gs.possTeam] += 1
                gs.lastCountedPossessionTeam = gs.possTeam
            if tipoffJustOccurred:
                gs.teamPossessionTime[gs.possTeam] += 1.0

            if gs.possTeam == t1:
                offense = t1
                defense = t2
                offense_df = gs.t1onCourt
                defense_df = gs.t2onCourt
                team_side = "HOME"
                actionParameters = {
                    "steal_cutoff": gs.lineupParameters["t1StealCutoff"],
                    "turnover_cutoff": gs.lineupParameters["t1TOCutoff"],
                    "move_cutoff": gs.lineupParameters["t1MoveCutoff"],
                    "pass_cutoff": gs.lineupParameters["t1PassCutoff"],
                    "shot_cutoff": gs.lineupParameters["t1ShotCutoff"],
                }
            else:
                offense = t2
                defense = t1
                offense_df = gs.t2onCourt
                defense_df = gs.t1onCourt
                team_side = "AWAY"
                actionParameters = {
                    "steal_cutoff": gs.lineupParameters["t2StealCutoff"],
                    "turnover_cutoff": gs.lineupParameters["t2TOCutoff"],
                    "move_cutoff": gs.lineupParameters["t2MoveCutoff"],
                    "pass_cutoff": gs.lineupParameters["t2PassCutoff"],
                    "shot_cutoff": gs.lineupParameters["t2ShotCutoff"],
                }

            if not tipoffJustOccurred and gs.checkTeamTimeout(gs.possTeam, False, gs.possPlayer):
                gs.defendedPlayerId = None
                gs.currentDefender = None
                gs.previousDefender = None
                continue

            attemptFinalHeave = False
            finalHeaveStartedAfterInbound = gs.finalHeavePending
            gs.finalHeavePending = False
            finalHeaveScoringDeficit = (gs.t2pts - gs.t1pts) if gs.possTeam == t1 else (gs.t1pts - gs.t2pts)

            if (
                not tipoffJustOccurred
                and gs.period >= gs.periodPerGame
                and 0 < gs.currTime <= finalHeaveMaximumTime
                and 0 <= finalHeaveScoringDeficit <= 3
            ):
                if finalHeaveStartedAfterInbound:
                    finalHeaveInbounder = gs.possPlayer
                    finalHeaveShooters = [
                        p for p in offense_df.values() if int(p["ID"]) != int(finalHeaveInbounder["ID"])
                    ]
                    if finalHeaveShooters:
                        weights = [max(0.01, float(p["shooting3"]) * float(p["bbiq"])) for p in finalHeaveShooters]
                        gs.possPlayer = random.choices(finalHeaveShooters, weights=weights, k=1)[0]
                    print(
                        f"With {gs.currTime:.1f} seconds remaining, {finalHeaveInbounder['position']} {finalHeaveInbounder['first_name']} {finalHeaveInbounder['last_name']} inbounds to {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} for a final heave."
                    )
                else:
                    print(
                        f"With {gs.currTime:.1f} seconds remaining, {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} recognizes the clock and prepares a final heave."
                    )
                attemptFinalHeave = True

            possPlayerId = int(gs.possPlayer["id"])
            if gs.defendedPlayerId != possPlayerId:
                gs.previousDefender = gs.currentDefender
                gs.currentDefender = selectDefender(
                    gs.possPlayer, offense_df, defense_df, excluded_defender=gs.previousDefender
                )
                gs.defendedPlayerId = possPlayerId
            defender = gs.currentDefender

            offense_slot = getOnCourtSlot(gs.possPlayer, offense_df)
            defense_slot = getOnCourtSlot(defender, defense_df)
            print(
                f"Matchup: {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} ({offense_slot}) vs {defender['position']} {defender['first_name']} {defender['last_name']} ({defense_slot})"
            )

            baseStealProbability = actionParameters["steal_cutoff"]
            baseTurnoverProbability = actionParameters["turnover_cutoff"] - actionParameters["steal_cutoff"]
            baseMoveProbability = actionParameters["move_cutoff"] - actionParameters["turnover_cutoff"]
            basePassProbability = actionParameters["pass_cutoff"] - actionParameters["move_cutoff"]
            baseShotProbability = max(0.0, 1.0 - actionParameters["pass_cutoff"])

            offensePace = gs.t1Pace if offense == t1 else gs.t2Pace
            activeDefensiveFormation = gs.t2DefensiveFormation if offense == t1 else gs.t1DefensiveFormation
            defensiveFocusPlayerId = gs.t2FocusPlayerId if offense == t1 else gs.t1FocusPlayerId
            focusPlayerOnCourt = defensiveFocusPlayerId is not None and any(
                int(p["id"]) == defensiveFocusPlayerId for p in offense_df.values()
            )
            if activeDefensiveFormation in gs.doubleTeamAdjustments and focusPlayerOnCourt:
                doubleTeamRole = "focus" if int(gs.possPlayer["id"]) == defensiveFocusPlayerId else "teammate"
                doubleTeamShotAdjustment = gs.doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole]["shot"]
                doubleTeamMovementAdjustment = gs.doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole][
                    "movement"
                ]
                doubleTeamPassDeflectionAdjustment = gs.doubleTeamAdjustments[activeDefensiveFormation][doubleTeamRole][
                    "pass_deflection"
                ]
            else:
                doubleTeamRole = "inactive"
                doubleTeamShotAdjustment = 0.0
                doubleTeamMovementAdjustment = 0.0
                doubleTeamPassDeflectionAdjustment = 0.0

            offenseShotClockUrgencyStart = gs.paceShotClockUrgencyStarts[gs.league][offensePace]
            shotClockUrgencyProgress = max(
                0.0, min(1.0, (offenseShotClockUrgencyStart - gs.currShotClock) / offenseShotClockUrgencyStart)
            )
            shotClockBBIQ = float(gs.possPlayer["bbiq"])
            shotClockBBIQDifference = shotClockBBIQ - shotClockAwarenessAverageBBIQ
            shotClockEffectiveBBIQDifference = max(
                -shotClockAwarenessMaximumBBIQGap, min(shotClockAwarenessMaximumBBIQGap, shotClockBBIQDifference)
            )
            shotClockAwarenessModifier = 1.0 + (shotClockEffectiveBBIQDifference * shotClockAwarenessModifierPerPoint)
            requestedShotClockUrgencyBonus = (
                shotClockUrgencyMaximumBonus * (shotClockUrgencyProgress**2) * shotClockAwarenessModifier
            )
            availableMovePassProbability = max(0.0, baseMoveProbability + basePassProbability)
            maximumShotClockTransfer = max(0.0, shotClockUrgencyMaximumShotProbability - baseShotProbability)
            shotClockUrgencyTransfer = min(
                requestedShotClockUrgencyBonus, maximumShotClockTransfer, availableMovePassProbability
            )
            remainingMovePassScale = (
                (availableMovePassProbability - shotClockUrgencyTransfer) / availableMovePassProbability
                if availableMovePassProbability > 0
                else 0.0
            )
            adjustedMoveProbability = baseMoveProbability * remainingMovePassScale
            adjustedPassProbability = basePassProbability * remainingMovePassScale
            adjustedShotProbability = baseShotProbability + shotClockUrgencyTransfer

            zone = get_shot_zone(gs.courtPos)
            preferenceZone = gs.getPreferenceZone(zone)
            activeLineupPreferences = gs.getActiveLineupPreferences(offense_df)
            playerShotPreference = None
            playerShotWillingnessAdjustment = 0.0
            playerShotWillingnessTransfer = 0.0
            if preferenceZone is not None and is_in_frontcourt(team_side, gs.courtPos):
                prefCol = {
                    "inside": "inside_preference",
                    "midrange": "midrange_preference",
                    "three": "three_preference",
                }[preferenceZone]
                playerShotPreference = float(gs.possPlayer[prefCol])
                playerShotWillingnessAdjustment = max(
                    -gs.playerShotWillingnessMaximumAdjustment,
                    min(
                        gs.playerShotWillingnessMaximumAdjustment,
                        (playerShotPreference - activeLineupPreferences[preferenceZone])
                        * gs.playerShotWillingnessPerProportionPoint,
                    ),
                )
                availableAMP = adjustedMoveProbability + adjustedPassProbability
                if playerShotWillingnessAdjustment > 0:
                    playerShotWillingnessTransfer = min(
                        playerShotWillingnessAdjustment,
                        availableAMP,
                        shotClockUrgencyMaximumShotProbability - adjustedShotProbability,
                    )
                    if availableAMP > 0:
                        wScale = (availableAMP - playerShotWillingnessTransfer) / availableAMP
                        adjustedMoveProbability *= wScale
                        adjustedPassProbability *= wScale
                    adjustedShotProbability += playerShotWillingnessTransfer
                elif playerShotWillingnessAdjustment < 0:
                    playerShotWillingnessTransfer = min(-playerShotWillingnessAdjustment, adjustedShotProbability)
                    adjustedShotProbability -= playerShotWillingnessTransfer
                    if availableAMP > 0:
                        adjustedMoveProbability += playerShotWillingnessTransfer * (
                            adjustedMoveProbability / availableAMP
                        )
                        adjustedPassProbability += playerShotWillingnessTransfer * (
                            adjustedPassProbability / availableAMP
                        )
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

            if gs.currShotClock <= offenseShotClockUrgencyStart and not attemptFinalHeave:
                print(
                    f"Shot-clock urgency: {gs.currShotClock:.1f}s | Pace: {offensePace} | Urgency begins: {offenseShotClockUrgencyStart:.1f}s | BBIQ: {shotClockBBIQ:.0f} | Awareness modifier: {shotClockAwarenessModifier:.3f} | Progress: {shotClockUrgencyProgress:.3f} | Base shot chance: {baseShotProbability:.2%} | Requested bonus: {requestedShotClockUrgencyBonus:.2%} | Actual transfer: {shotClockUrgencyTransfer:.2%} | Adjusted shot chance: {adjustedShotProbability:.2%} | Roll: {actionRoll:.4f} | Action: {action.upper()}"
                )
            if playerShotPreference is not None and not attemptFinalHeave:
                print(
                    f"Shot preference: {preferenceZone} | Player: {playerShotPreference:.1f}% | Active lineup: {activeLineupPreferences[preferenceZone]:.1f}% | Requested adjustment: {playerShotWillingnessAdjustment:+.2%} | Actual transfer: {math.copysign(playerShotWillingnessTransfer, playerShotWillingnessAdjustment):+.2%} | Final shot chance: {adjustedShotProbability:.2%}"
                )

            took_shot = False
            in_frontcourt = is_in_frontcourt(team_side, gs.courtPos)
            if action == "shot" and (zone is None or not in_frontcourt):
                action = "pass" if gs.crossed_midcourt else "move"

            if attemptFinalHeave:
                randTime = gs.currTime
            else:
                paceCat = random.choices(
                    gs.paceActionTimeCategories, weights=gs.paceActionTimeWeights[offensePace], k=1
                )[0]
                paceATM = gs.paceActionTimeModifiers[paceCat]
                availableActionTime = max(0.0, min(gs.currShotClock, gs.currTime))
                minAT = max(0.25, 0.439 * paceATM)
                maxAT = 3.33 * paceATM
                if availableActionTime >= 2:
                    randTime = round(
                        random.uniform(min(minAT, min(maxAT, availableActionTime)), min(maxAT, availableActionTime)), 2
                    )
                elif availableActionTime > 0.25:
                    randTime = round(min(availableActionTime, max(0.25, 1.0 * paceATM)), 2)
                else:
                    randTime = availableActionTime

            elapsedTime = (
                gs.currTime
                if attemptFinalHeave
                else (
                    availableActionTime
                    if round(randTime, 2) <= 0 < availableActionTime
                    else min(availableActionTime, round(randTime, 2))
                )
            )
            gs.addPlayingTime(elapsedTime)
            gs.teamPossessionTime[offense] += elapsedTime
            gs.currTime = max(0.0, gs.currTime - elapsedTime)
            gs.currShotClock = max(0.0, gs.currShotClock - elapsedTime)

            shotClockQualityAdjustment = 0.0
            shotClockQualityLabel = "normal window"
            if gs.league == "CBB":
                if gs.currShotClock >= 26:
                    shotClockQualityAdjustment = -0.020
                    shotClockQualityLabel = "extremely early"
                elif gs.currShotClock >= 22:
                    shotClockQualityAdjustment = -0.010
                    shotClockQualityLabel = "early"
                elif gs.currShotClock < 3:
                    shotClockQualityAdjustment = -0.015
                    shotClockQualityLabel = "desperation"
                elif gs.currShotClock < 6:
                    shotClockQualityAdjustment = -0.005
                    shotClockQualityLabel = "late"
            else:
                if gs.currShotClock >= 21:
                    shotClockQualityAdjustment = -0.020
                    shotClockQualityLabel = "extremely early"
                elif gs.currShotClock >= 18:
                    shotClockQualityAdjustment = -0.010
                    shotClockQualityLabel = "early"
                elif gs.currShotClock < 2.5:
                    shotClockQualityAdjustment = -0.015
                    shotClockQualityLabel = "desperation"
                elif gs.currShotClock < 5:
                    shotClockQualityAdjustment = -0.005
                    shotClockQualityLabel = "late"

            if gs.currTime < 60:
                game_clock_text = f"00:{max(0.0, gs.currTime):04.1f}"
            else:
                dm = max(0, math.ceil(gs.currTime))
                game_clock_text = f"{dm // 60:02d}:{dm % 60:02d}"
            display_shot_clock = max(0.0, gs.currShotClock)
            shot_clock_text = (
                f"{display_shot_clock:04.1f}" if display_shot_clock < 10 else f"{math.ceil(display_shot_clock):02d}"
            )

            if action == "heave":
                gs.currTime = 0
                gs.currShotClock = 0
                gs.assistPlayer = None
                took_shot = True
                heaveStats = gs.t1stats if offense == t1 else gs.t2stats
                heaveShooterMinutes = float(heaveStats.at[gs.possPlayer["id"].item(), "MP"]) / 60
                heaveRecoveryMinutes = gs.getPlayerRecoveryMinutes(gs.possPlayer)
                heaveFatigueMinutes = max(0.0, heaveShooterMinutes - heaveRecoveryMinutes)
                (
                    heaveShootingRating,
                    baseHeaveShootingRating,
                    heaveStaminaCapacity,
                    heaveShooterMinutes,
                    heaveStaminaUsageRatio,
                    heaveFatiguePenalty,
                    heaveStaminaModifier,
                ) = get_stamina_adjusted_rating(gs.possPlayer, "shooting3", heaveShooterMinutes, heaveRecoveryMinutes)
                staminaAdjustedHeave = heaveShootingRating
                heaveShootingRating, heaveMomentumStrength, heaveMomentumBonus, heaveMomentumModifier = (
                    gs.getMomentumAdjustedRating(staminaAdjustedHeave, offense)
                )
                normalHeaveChance = (0.008 * heaveShootingRating) + 0.13
                if offense == t1:
                    normalHeaveChance += gs.HCAAdj
                heaveChance = max(
                    finalHeaveMinimumChance,
                    min(finalHeaveMaximumChance, normalHeaveChance * finalHeaveDifficultyMultiplier),
                )
                heaveRoll = random.random()
                heaveMade = heaveRoll < heaveChance
                if offense == t1:
                    gs.t1stats.at[gs.possPlayer["id"].item(), "3PT Shot Att"] += 1
                    gs.t13a += 1
                else:
                    gs.t2stats.at[gs.possPlayer["id"].item(), "3PT Shot Att"] += 1
                    gs.t23a += 1
                print(
                    f"{gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} launches a desperation heave from beyond half court!"
                )
                print(
                    f"Final heave: shooting3 {heaveShootingRating:.4f} [base {baseHeaveShootingRating:.2f}; stamina adjusted {staminaAdjustedHeave:.4f}; MP {heaveShooterMinutes:.2f}; recovery {heaveRecoveryMinutes:.2f}; fatigue load {heaveFatigueMinutes:.2f}/{heaveStaminaCapacity:.2f}; stamina modifier {heaveStaminaModifier:.3f}; momentum {heaveMomentumStrength:.0%}; momentum bonus {heaveMomentumBonus:.2%}; momentum modifier {heaveMomentumModifier:.3f}] | Normal 3PT chance: {normalHeaveChance:.2%} | Heave multiplier: {finalHeaveDifficultyMultiplier:.3f} | Heave chance: {heaveChance:.2%} | Roll: {heaveRoll:.4f}"
                )
                if heaveMade:
                    if offense == t1:
                        gs.t1pts += 3
                        gs.t13m += 1
                        gs.t1stats.at[gs.possPlayer["id"].item(), "3PT Shot Made"] += 1
                        if gs.period == 1:
                            gs.t1q1pts += 3
                        elif gs.period == 2:
                            gs.t1q2pts += 3
                        elif gs.league != "CBB" and gs.period == 3:
                            gs.t1q3pts += 3
                        elif gs.league != "CBB" and gs.period == 4:
                            gs.t1q4pts += 3
                        elif gs.period > gs.periodPerGame:
                            gs.t1qotpts += 3
                    else:
                        gs.t2pts += 3
                        gs.t23m += 1
                        gs.t2stats.at[gs.possPlayer["id"].item(), "3PT Shot Made"] += 1
                        if gs.period == 1:
                            gs.t2q1pts += 3
                        elif gs.period == 2:
                            gs.t2q2pts += 3
                        elif gs.league != "CBB" and gs.period == 3:
                            gs.t2q3pts += 3
                        elif gs.league != "CBB" and gs.period == 4:
                            gs.t2q4pts += 3
                        elif gs.period > gs.periodPerGame:
                            gs.t2qotpts += 3
                    print("...GOOD! IT COUNTS AT THE BUZZER!")
                    gs.adjustMomentum(offense, momentumMadeThreeSwing, "made final heave")
                else:
                    print("...OFF THE MARK! The horn sounds.")
                    gs.adjustMomentum(defense, momentumMissSwing, "missed final heave")

            if zone is not None and in_frontcourt:
                if action == "shot":
                    zone = get_shot_zone(gs.courtPos)
                    in_frontcourt = is_in_frontcourt(team_side, gs.courtPos)
                    if zone is not None and in_frontcourt:
                        shootPlayer = gs.possPlayer
                        offenseStats = gs.t1stats if offense == t1 else gs.t2stats
                        defenseStats = gs.t2stats if offense == t1 else gs.t1stats
                        shootPlayerMinutes = float(offenseStats.at[shootPlayer["id"].item(), "MP"]) / 60
                        defenderMinutes = float(defenseStats.at[defender["id"].item(), "MP"]) / 60
                        shootPlayerRecoveryMinutes = gs.getPlayerRecoveryMinutes(shootPlayer)
                        defenderRecoveryMinutes = gs.getPlayerRecoveryMinutes(defender)
                        shootPlayerFatigueMinutes = max(0.0, shootPlayerMinutes - shootPlayerRecoveryMinutes)
                        defenderFatigueMinutes = max(0.0, defenderMinutes - defenderRecoveryMinutes)
                        (
                            _,
                            _,
                            defenderStaminaCapacity,
                            defenderMinutes,
                            defenderStaminaUsageRatio,
                            defenderFatiguePenalty,
                            defenderStaminaModifier,
                        ) = get_stamina_adjusted_rating(
                            defender, "perimeter_defense", defenderMinutes, defenderRecoveryMinutes
                        )
                        baseBlockRating = float(defender["block"])

                        if zone in ["three", "corner_three"]:
                            shotOffenseType = "shooting3"
                            (
                                shotOffense,
                                baseShotOffense,
                                shooterStaminaCapacity,
                                shootPlayerMinutes,
                                shooterStaminaUsageRatio,
                                shooterFatiguePenalty,
                                shooterStaminaModifier,
                            ) = get_stamina_adjusted_rating(
                                shootPlayer, shotOffenseType, shootPlayerMinutes, shootPlayerRecoveryMinutes
                            )
                            staminaAdjustedShotOffense = shotOffense
                            shotOffense, shotMomentumStrength, shotMomentumBonus, shotMomentumModifier = (
                                gs.getMomentumAdjustedRating(staminaAdjustedShotOffense, offense)
                            )
                            baseShotChance = (0.008 * shotOffense) + 0.180
                            if offense == t1:
                                baseShotChance += gs.HCAAdj
                            shotDefenseAdjustment, shotDefense, shotDefenseType = get_shot_defense_adjustment(
                                defender, gs.courtPos, defenderStaminaModifier
                            )
                            madeShot = max(
                                0.0,
                                min(
                                    1.0,
                                    baseShotChance
                                    + shotDefenseAdjustment
                                    + shotClockQualityAdjustment
                                    + doubleTeamShotAdjustment,
                                ),
                            )
                            shootingFoulChance, zoneFoulBaseline, foulDefenderIQ, bbiqFoulModifier = (
                                get_shooting_foul_chance(defender, gs.courtPos)
                            )
                            shootingFoulRoll = random.random()
                            shootingFoul = shootingFoulRoll < shootingFoulChance
                            defenderFouledOut = False
                            defenderFoulProtected = False
                            if shootingFoul:
                                defenderStatId = defender["id"].item()
                                defenderPlayerId = int(defender["ID"])
                                if offense == t1:
                                    gs.t2stats.at[defenderStatId, "Foul"] += 1
                                    if gs.period == 1:
                                        gs.t2FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t2FirstHalfTeamFouls
                                    else:
                                        gs.t2SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t2SecondHalfTeamFouls
                                    defenderFoulTotal = int(gs.t2stats.at[defenderStatId, "Foul"])
                                    if (
                                        defenderFoulTotal >= gs.foulOutLimit
                                        and defenderPlayerId not in gs.t2FouledOutPlayerIds
                                    ):
                                        gs.t2FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = gs.registerFoulProtection(
                                        2,
                                        defenderStatId,
                                        defenderPlayerId,
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                    )
                                else:
                                    gs.t1stats.at[defenderStatId, "Foul"] += 1
                                    if gs.period == 1:
                                        gs.t1FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t1FirstHalfTeamFouls
                                    else:
                                        gs.t1SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t1SecondHalfTeamFouls
                                    defenderFoulTotal = int(gs.t1stats.at[defenderStatId, "Foul"])
                                    if (
                                        defenderFoulTotal >= gs.foulOutLimit
                                        and defenderPlayerId not in gs.t1FouledOutPlayerIds
                                    ):
                                        gs.t1FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = gs.registerFoulProtection(
                                        1,
                                        defenderStatId,
                                        defenderPlayerId,
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                    )
                                print(f"Defending team fouls this half: {defendingHalfTeamFouls}")
                                if defenderFouledOut:
                                    print(
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!"
                                    )
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
                                (
                                    blockChance,
                                    zoneBlockBaseline,
                                    blockRating,
                                    blockRatingAdjustment,
                                    defenderHeight,
                                    shooterHeight,
                                    heightAdjustment,
                                ) = get_block_chance(defender, shootPlayer, gs.courtPos, defenderStaminaModifier)
                                blockRoll = random.random()
                                shotBlocked = blockRoll < blockChance
                            shotRand = None if shotBlocked else random.random()
                            if shootingFoul:
                                madeShot *= shootingFoulMadeShotModifier
                            shotMade = not shotBlocked and shotRand is not None and shotRand < madeShot
                            print(
                                f"Shot offense: {shotOffense:.4f} [{shotOffenseType}; base {baseShotOffense:.2f}; stamina adjusted {staminaAdjustedShotOffense:.4f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; stamina modifier {shooterStaminaModifier:.3f}; momentum {shotMomentumStrength:.0%}; momentum bonus {shotMomentumBonus:.2%}; momentum modifier {shotMomentumModifier:.3f}] | Shot defense: {shotDefense:.4f} [{shotDefenseType}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Defense adjustment: {shotDefenseAdjustment:+.2%} | Shot-clock quality: {shotClockQualityLabel} {shotClockQualityAdjustment:+.2%} | Double-team role: {doubleTeamRole} {doubleTeamShotAdjustment:+.2%} | Final shot chance: {madeShot:.2%} | Roll: {'SKIPPED' if shotRand is None else f'{shotRand:.4f}'}"
                            )
                            print(
                                f"Shooting foul baseline: {zoneFoulBaseline:.2%} | Defender BBIQ: {foulDefenderIQ:.0f} | BBIQ modifier: {bbiqFoulModifier:.3f} | Foul chance: {shootingFoulChance:.2%} | Foul roll: {shootingFoulRoll:.4f} | {'FOUL' if shootingFoul else 'NO FOUL'}"
                            )
                            print(
                                f"Block rating: {blockRating:.4f} [base {baseBlockRating:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; modifier {defenderStaminaModifier:.3f}] | Zone baseline: {zoneBlockBaseline:.2%} | Rating adjustment: {blockRatingAdjustment:+.2%} | Height: {defenderHeight:.0f} vs {shooterHeight:.0f} | Height adjustment: {heightAdjustment:+.2%} | Block chance: {blockChance:.2%} | Block roll: {'SKIPPED' if blockRoll is None else f'{blockRoll:.4f}'} | {'BLOCKED' if shotBlocked else 'NOT BLOCKED'}"
                            )
                            if not shootingFoul or shotMade:
                                if offense == t1:
                                    gs.t1stats.at[shootPlayer["id"].item(), "3PT Shot Att"] += 1
                                    gs.t13a += 1
                                else:
                                    gs.t2stats.at[shootPlayer["id"].item(), "3PT Shot Att"] += 1
                                    gs.t23a += 1
                            print(
                                periodLabel
                                + ": "
                                + game_clock_text
                                + " / Shot Clock: :"
                                + shot_clock_text
                                + " ("
                                + gs.possTeam
                                + ")"
                            )
                            print(
                                f"3-point attempt from {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']}"
                            )
                            if shotMade:
                                if offense == t1:
                                    gs.t1pts += 3
                                    gs.t13m += 1
                                    gs.t1stats.at[shootPlayer["id"].item(), "3PT Shot Made"] += 1
                                    if gs.assistPlayer is not None:
                                        gs.t1stats.at[gs.assistPlayer["id"].item(), "Assist"] += 1
                                    if gs.period == 1:
                                        gs.t1q1pts += 3
                                    elif gs.period == 2:
                                        gs.t1q2pts += 3
                                    elif gs.league != "CBB" and gs.period == 3:
                                        gs.t1q3pts += 3
                                    elif gs.league != "CBB" and gs.period == 4:
                                        gs.t1q4pts += 3
                                    elif gs.period > gs.periodPerGame:
                                        gs.t1qotpts += 3
                                else:
                                    gs.t2pts += 3
                                    gs.t23m += 1
                                    gs.t2stats.at[shootPlayer["id"].item(), "3PT Shot Made"] += 1
                                    if gs.assistPlayer is not None:
                                        gs.t2stats.at[gs.assistPlayer["id"].item(), "Assist"] += 1
                                    if gs.period == 1:
                                        gs.t2q1pts += 3
                                    elif gs.period == 2:
                                        gs.t2q2pts += 3
                                    elif gs.league != "CBB" and gs.period == 3:
                                        gs.t2q3pts += 3
                                    elif gs.league != "CBB" and gs.period == 4:
                                        gs.t2q4pts += 3
                                    elif gs.period > gs.periodPerGame:
                                        gs.t2qotpts += 3
                                print(
                                    "...GOOD! Assisted by "
                                    + gs.assistPlayer["position"]
                                    + " "
                                    + gs.assistPlayer["first_name"]
                                    + " "
                                    + gs.assistPlayer["last_name"]
                                    if gs.assistPlayer is not None
                                    else "...GOOD!"
                                )
                                gs.adjustMomentum(offense, momentumMadeThreeSwing, "made three-point shot")
                            else:
                                if shotBlocked:
                                    if offense == t1:
                                        gs.t2stats.at[defender["id"].item(), "Blk"] += 1
                                    else:
                                        gs.t1stats.at[defender["id"].item(), "Blk"] += 1
                                    print(
                                        f"...BLOCKED by {defender['position']} {defender['first_name']} {defender['last_name']}!"
                                    )
                                    gs.adjustMomentum(defense, momentumBlockSwing, "blocked three-point shot")
                                elif shootingFoul:
                                    print("...MISSED, but a shooting foul is called!")
                                    gs.adjustMomentum(defense, momentumMissSwing, "missed three-point shot")
                                else:
                                    print("...MISSED!")
                                    gs.adjustMomentum(defense, momentumMissSwing, "missed three-point shot")
                            gs.assistPlayer = None
                            freeThrowsAwarded = 0
                            lastFreeThrowMade = False
                            if shootingFoul:
                                freeThrowsAwarded = 1 if shotMade else 3
                                print(
                                    f"FOUL on {defender['position']} {defender['first_name']} {defender['last_name']}! {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} will shoot {freeThrowsAwarded} free throw{'s' if freeThrowsAwarded != 1 else ''}."
                                )
                                ftMediaTimeout = gs.checkTimeoutStoppage(offense, True, shootPlayer)
                                ftSubsCompleted = ftMediaTimeout
                                if (defenderFouledOut or defenderFoulProtected) and not ftSubsCompleted:
                                    gs.pullFreeThrowSubs(shootPlayer)
                                    ftSubsCompleted = True
                                    gs.defendedPlayerId = None
                                    gs.currentDefender = None
                                    gs.previousDefender = None
                                elif freeThrowsAwarded == 1 and not ftSubsCompleted:
                                    gs.pullFreeThrowSubs(shootPlayer)
                                    ftSubsCompleted = True
                                if offense == t1:
                                    offense_df = gs.t1onCourt
                                    defense_df = gs.t2onCourt
                                    ftStats = gs.t1stats
                                else:
                                    offense_df = gs.t2onCourt
                                    defense_df = gs.t1onCourt
                                    ftStats = gs.t2stats
                                shootPlayerMinutes = float(ftStats.at[shootPlayer["id"].item(), "MP"]) / 60
                                shootPlayerRecoveryMinutes = gs.getPlayerRecoveryMinutes(shootPlayer)
                                shootPlayerFatigueMinutes = max(0.0, shootPlayerMinutes - shootPlayerRecoveryMinutes)
                                (
                                    _,
                                    _,
                                    shooterStaminaCapacity,
                                    shootPlayerMinutes,
                                    shooterStaminaUsageRatio,
                                    shooterFatiguePenalty,
                                    shooterStaminaModifier,
                                ) = get_stamina_adjusted_rating(
                                    shootPlayer, "free_throw", shootPlayerMinutes, shootPlayerRecoveryMinutes
                                )
                                ftHCA = gs.HCAAdj if offense == t1 else 0
                                for ftNum in range(1, freeThrowsAwarded + 1):
                                    ftMade, ftChance, ftRoll, ftRating, baseFTRating = resolve_free_throw(
                                        shootPlayer, ftHCA, shooterStaminaModifier
                                    )
                                    if offense == t1:
                                        gs.t1stats.at[shootPlayer["id"].item(), "FT Shot Att"] += 1
                                    else:
                                        gs.t2stats.at[shootPlayer["id"].item(), "FT Shot Att"] += 1
                                    if ftMade:
                                        if offense == t1:
                                            gs.t1pts += 1
                                            gs.t1stats.at[shootPlayer["id"].item(), "FT Shot Made"] += 1
                                            if gs.period == 1:
                                                gs.t1q1pts += 1
                                            elif gs.period == 2:
                                                gs.t1q2pts += 1
                                            elif gs.league != "CBB" and gs.period == 3:
                                                gs.t1q3pts += 1
                                            elif gs.league != "CBB" and gs.period == 4:
                                                gs.t1q4pts += 1
                                            elif gs.period > gs.periodPerGame:
                                                gs.t1qotpts += 1
                                        else:
                                            gs.t2pts += 1
                                            gs.t2stats.at[shootPlayer["id"].item(), "FT Shot Made"] += 1
                                            if gs.period == 1:
                                                gs.t2q1pts += 1
                                            elif gs.period == 2:
                                                gs.t2q2pts += 1
                                            elif gs.league != "CBB" and gs.period == 3:
                                                gs.t2q3pts += 1
                                            elif gs.league != "CBB" and gs.period == 4:
                                                gs.t2q4pts += 1
                                            elif gs.period > gs.periodPerGame:
                                                gs.t2qotpts += 1
                                    print(
                                        f"Free throw {ftNum} of {freeThrowsAwarded}: rating {ftRating:.4f} [base {baseFTRating:.2f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; modifier {shooterStaminaModifier:.3f}] | Chance: {ftChance:.2%} | Roll: {ftRoll:.4f} | {'GOOD' if ftMade else 'MISSED'}"
                                    )
                                    lastFreeThrowMade = ftMade
                                    if ftNum == 1 and freeThrowsAwarded > 1 and not ftSubsCompleted:
                                        gs.pullFreeThrowSubs(shootPlayer)
                                        ftSubsCompleted = True
                                        if offense == t1:
                                            offense_df = gs.t1onCourt
                                            defense_df = gs.t2onCourt
                                        else:
                                            offense_df = gs.t2onCourt
                                            defense_df = gs.t1onCourt
                            needsRebound = (not shootingFoul and not shotMade) or (
                                shootingFoul and not lastFreeThrowMade
                            )
                            if needsRebound:
                                rebRand = random.random()
                                offensiveReboundChance = gs.lineupParameters[
                                    "t1OffensiveRebound" if offense == t1 else "t2OffensiveRebound"
                                ]
                                if rebRand < offensiveReboundChance:
                                    pickRebounder = random.choice(list(offense_df.values()))
                                    while pickRebounder["id"] == shootPlayer["id"]:
                                        pickRebounder = random.choice(list(offense_df.values()))
                                    gs.possPlayer = pickRebounder
                                    if offense == t1:
                                        gs.t1stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                    else:
                                        gs.t2stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                    print(
                                        gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " grabs the offensive rebound for "
                                        + gs.possTeam
                                    )
                                    gs.currShotClock = gs.shotClockReset
                                    if gs.currTime < gs.currShotClock:
                                        gs.currShotClock = gs.currTime
                                else:
                                    gs.possPlayer = random.choice(list(defense_df.values()))
                                    if offense == t1:
                                        gs.t2stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                        gs.possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = gs.t2onCourt
                                        defense_df = gs.t1onCourt
                                        gs.courtPos = (random.randint(2, 4), random.randint(2, 4))
                                    else:
                                        gs.t1stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                        gs.possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = gs.t1onCourt
                                        defense_df = gs.t2onCourt
                                        gs.courtPos = (random.randint(2, 4) * -1, random.randint(2, 4))
                                    gs.currShotClock = gs.shotClock
                                    if gs.currTime <= gs.shotClock:
                                        gs.currShotClock = gs.currTime
                                    gs.crossed_midcourt = False
                                    print(
                                        gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " grabs the defensive rebound for "
                                        + gs.possTeam
                                    )
                                    gs.defendedPlayerId = None
                                    gs.currentDefender = None
                                    gs.previousDefender = None
                            else:
                                if offense == t1:
                                    gs.possTeam = t2
                                    offense_df = gs.t2onCourt
                                    defense_df = gs.t1onCourt
                                    gs.courtPos = (4, 3)
                                    gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                                else:
                                    gs.possTeam = t1
                                    offense_df = gs.t1onCourt
                                    defense_df = gs.t2onCourt
                                    gs.courtPos = (-4, 3)
                                    gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                                gs.crossed_midcourt = False
                                gs.currShotClock = gs.shotClock
                                if gs.currTime <= gs.shotClock:
                                    gs.currShotClock = gs.currTime
                                print(
                                    gs.possPlayer["position"]
                                    + " "
                                    + gs.possPlayer["first_name"]
                                    + " "
                                    + gs.possPlayer["last_name"]
                                    + " takes the ball out for "
                                    + gs.possTeam
                                )
                                gs.finalHeavePending = True
                                gs.defendedPlayerId = None
                                gs.currentDefender = None
                                gs.previousDefender = None
                            print(t1 + ": " + str(gs.t1pts) + " / " + t2 + ": " + str(gs.t2pts))
                            print(footerPos)
                            gs.printMomentumMeter()
                            took_shot = True

                        elif zone in ["inside", "paint", "midrange"]:
                            if zone == "midrange":
                                shotOffenseType = "shooting2"
                                (
                                    shotOffense,
                                    baseShotOffense,
                                    shooterStaminaCapacity,
                                    shootPlayerMinutes,
                                    shooterStaminaUsageRatio,
                                    shooterFatiguePenalty,
                                    shooterStaminaModifier,
                                ) = get_stamina_adjusted_rating(
                                    shootPlayer, shotOffenseType, shootPlayerMinutes, shootPlayerRecoveryMinutes
                                )
                                staminaAdjustedShotOffense = shotOffense
                                shotOffense, shotMomentumStrength, shotMomentumBonus, shotMomentumModifier = (
                                    gs.getMomentumAdjustedRating(staminaAdjustedShotOffense, offense)
                                )
                                baseShotChance = (0.0074 * shotOffense) + 0.265
                            else:
                                shotOffenseType = "finishing"
                                (
                                    shotOffense,
                                    baseShotOffense,
                                    shooterStaminaCapacity,
                                    shootPlayerMinutes,
                                    shooterStaminaUsageRatio,
                                    shooterFatiguePenalty,
                                    shooterStaminaModifier,
                                ) = get_stamina_adjusted_rating(
                                    shootPlayer, shotOffenseType, shootPlayerMinutes, shootPlayerRecoveryMinutes
                                )
                                staminaAdjustedShotOffense = shotOffense
                                shotOffense, shotMomentumStrength, shotMomentumBonus, shotMomentumModifier = (
                                    gs.getMomentumAdjustedRating(staminaAdjustedShotOffense, offense)
                                )
                                baseShotChance = (0.011 * shotOffense) + 0.39
                            if offense == t1:
                                baseShotChance += gs.HCAAdj
                            shotDefenseAdjustment, shotDefense, shotDefenseType = get_shot_defense_adjustment(
                                defender, gs.courtPos, defenderStaminaModifier
                            )
                            madeShot = max(
                                0.0,
                                min(
                                    1.0,
                                    baseShotChance
                                    + shotDefenseAdjustment
                                    + shotClockQualityAdjustment
                                    + doubleTeamShotAdjustment,
                                ),
                            )
                            shootingFoulChance, zoneFoulBaseline, foulDefenderIQ, bbiqFoulModifier = (
                                get_shooting_foul_chance(defender, gs.courtPos)
                            )
                            shootingFoulRoll = random.random()
                            shootingFoul = shootingFoulRoll < shootingFoulChance
                            defenderFouledOut = False
                            defenderFoulProtected = False
                            if shootingFoul:
                                defenderStatId = defender["id"].item()
                                defenderPlayerId = int(defender["ID"])
                                if offense == t1:
                                    gs.t2stats.at[defenderStatId, "Foul"] += 1
                                    if gs.period == 1:
                                        gs.t2FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t2FirstHalfTeamFouls
                                    else:
                                        gs.t2SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t2SecondHalfTeamFouls
                                    defenderFoulTotal = int(gs.t2stats.at[defenderStatId, "Foul"])
                                    if (
                                        defenderFoulTotal >= gs.foulOutLimit
                                        and defenderPlayerId not in gs.t2FouledOutPlayerIds
                                    ):
                                        gs.t2FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = gs.registerFoulProtection(
                                        2,
                                        defenderStatId,
                                        defenderPlayerId,
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                    )
                                else:
                                    gs.t1stats.at[defenderStatId, "Foul"] += 1
                                    if gs.period == 1:
                                        gs.t1FirstHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t1FirstHalfTeamFouls
                                    else:
                                        gs.t1SecondHalfTeamFouls += 1
                                        defendingHalfTeamFouls = gs.t1SecondHalfTeamFouls
                                    defenderFoulTotal = int(gs.t1stats.at[defenderStatId, "Foul"])
                                    if (
                                        defenderFoulTotal >= gs.foulOutLimit
                                        and defenderPlayerId not in gs.t1FouledOutPlayerIds
                                    ):
                                        gs.t1FouledOutPlayerIds.add(defenderPlayerId)
                                        defenderFouledOut = True
                                    defenderFoulProtected = gs.registerFoulProtection(
                                        1,
                                        defenderStatId,
                                        defenderPlayerId,
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                    )
                                print(f"Defending team fouls this half: {defendingHalfTeamFouls}")
                                if defenderFouledOut:
                                    print(
                                        f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!"
                                    )
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
                                (
                                    blockChance,
                                    zoneBlockBaseline,
                                    blockRating,
                                    blockRatingAdjustment,
                                    defenderHeight,
                                    shooterHeight,
                                    heightAdjustment,
                                ) = get_block_chance(defender, shootPlayer, gs.courtPos, defenderStaminaModifier)
                                blockRoll = random.random()
                                shotBlocked = blockRoll < blockChance
                            shotRand = None if shotBlocked else random.random()
                            if shootingFoul:
                                madeShot *= shootingFoulMadeShotModifier
                            shotMade = not shotBlocked and shotRand is not None and shotRand < madeShot
                            print(
                                f"Shot offense: {shotOffense:.4f} [{shotOffenseType}; base {baseShotOffense:.2f}; stamina adjusted {staminaAdjustedShotOffense:.4f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; stamina modifier {shooterStaminaModifier:.3f}; momentum {shotMomentumStrength:.0%}; momentum bonus {shotMomentumBonus:.2%}; momentum modifier {shotMomentumModifier:.3f}] | Shot defense: {shotDefense:.4f} [{shotDefenseType}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Defense adjustment: {shotDefenseAdjustment:+.2%} | Shot-clock quality: {shotClockQualityLabel} {shotClockQualityAdjustment:+.2%} | Double-team role: {doubleTeamRole} {doubleTeamShotAdjustment:+.2%} | Final shot chance: {madeShot:.2%} | Roll: {'SKIPPED' if shotRand is None else f'{shotRand:.4f}'}"
                            )
                            print(
                                f"Shooting foul baseline: {zoneFoulBaseline:.2%} | Defender BBIQ: {foulDefenderIQ:.0f} | BBIQ modifier: {bbiqFoulModifier:.3f} | Foul chance: {shootingFoulChance:.2%} | Foul roll: {shootingFoulRoll:.4f} | {'FOUL' if shootingFoul else 'NO FOUL'}"
                            )
                            print(
                                f"Block rating: {blockRating:.4f} [base {baseBlockRating:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; modifier {defenderStaminaModifier:.3f}] | Zone baseline: {zoneBlockBaseline:.2%} | Rating adjustment: {blockRatingAdjustment:+.2%} | Height: {defenderHeight:.0f} vs {shooterHeight:.0f} | Height adjustment: {heightAdjustment:+.2%} | Block chance: {blockChance:.2%} | Block roll: {'SKIPPED' if blockRoll is None else f'{blockRoll:.4f}'} | {'BLOCKED' if shotBlocked else 'NOT BLOCKED'}"
                            )
                            if not shootingFoul or shotMade:
                                if offense == t1:
                                    gs.t12a += 1
                                    if zone == "midrange":
                                        gs.t1stats.at[shootPlayer["id"].item(), "Mid Shot Att"] += 1
                                    else:
                                        gs.t1stats.at[shootPlayer["id"].item(), "Ins Shot Att"] += 1
                                else:
                                    gs.t22a += 1
                                    if zone == "midrange":
                                        gs.t2stats.at[shootPlayer["id"].item(), "Mid Shot Att"] += 1
                                    else:
                                        gs.t2stats.at[shootPlayer["id"].item(), "Ins Shot Att"] += 1
                            print(
                                periodLabel
                                + ": "
                                + game_clock_text
                                + " / Shot Clock: :"
                                + shot_clock_text
                                + " ("
                                + gs.possTeam
                                + ")"
                            )
                            print(
                                f"2-point attempt from {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']}"
                            )
                            if shotMade:
                                madeShotResult = "normal"
                                shotMakeQuality = shotRand / madeShot if madeShot > 0 else 1.0
                                if zone == "inside" and shotMakeQuality < insideDunkThreshold:
                                    madeShotResult = "inside_dunk"
                                elif zone == "paint":
                                    if shotMakeQuality < paintPosterDunkThreshold:
                                        madeShotResult = "paint_poster_dunk"
                                    elif shotMakeQuality < paintDriveDunkThreshold:
                                        madeShotResult = "paint_drive_dunk"
                                if offense == t1:
                                    gs.t1pts += 2
                                    gs.t12m += 1
                                    if zone == "midrange":
                                        gs.t1stats.at[shootPlayer["id"].item(), "Mid Shot Made"] += 1
                                    else:
                                        gs.t1stats.at[shootPlayer["id"].item(), "Ins Shot Made"] += 1
                                    if gs.assistPlayer is not None:
                                        gs.t1stats.at[gs.assistPlayer["id"].item(), "Assist"] += 1
                                    if gs.period == 1:
                                        gs.t1q1pts += 2
                                    elif gs.period == 2:
                                        gs.t1q2pts += 2
                                    elif gs.league != "CBB" and gs.period == 3:
                                        gs.t1q3pts += 2
                                    elif gs.league != "CBB" and gs.period == 4:
                                        gs.t1q4pts += 2
                                    elif gs.period > gs.periodPerGame:
                                        gs.t1qotpts += 2
                                else:
                                    gs.t2pts += 2
                                    gs.t22m += 1
                                    if zone == "midrange":
                                        gs.t2stats.at[shootPlayer["id"].item(), "Mid Shot Made"] += 1
                                    else:
                                        gs.t2stats.at[shootPlayer["id"].item(), "Ins Shot Made"] += 1
                                    if gs.assistPlayer is not None:
                                        gs.t2stats.at[gs.assistPlayer["id"].item(), "Assist"] += 1
                                    if gs.period == 1:
                                        gs.t2q1pts += 2
                                    elif gs.period == 2:
                                        gs.t2q2pts += 2
                                    elif gs.league != "CBB" and gs.period == 3:
                                        gs.t2q3pts += 2
                                    elif gs.league != "CBB" and gs.period == 4:
                                        gs.t2q4pts += 2
                                    elif gs.period > gs.periodPerGame:
                                        gs.t2qotpts += 2
                                assistText = (
                                    f" Assisted by {gs.assistPlayer['position']} {gs.assistPlayer['first_name']} {gs.assistPlayer['last_name']}."
                                    if gs.assistPlayer is not None
                                    else ""
                                )
                                if madeShotResult == "inside_dunk":
                                    print(
                                        f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} slams it home!{assistText}"
                                    )
                                elif madeShotResult == "paint_poster_dunk":
                                    print(
                                        f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} drives forward and POSTERIZES {defender['position']} {defender['first_name']} {defender['last_name']}! THE DISRESPECT!{assistText}"
                                    )
                                elif madeShotResult == "paint_drive_dunk":
                                    print(
                                        f"...{shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} drives forward and throws it down!{assistText}"
                                    )
                                elif gs.assistPlayer is not None:
                                    print(
                                        f"...GOOD! Assisted by {gs.assistPlayer['position']} {gs.assistPlayer['first_name']} {gs.assistPlayer['last_name']}"
                                    )
                                else:
                                    print("...GOOD!")
                                if madeShotResult in ("inside_dunk", "paint_drive_dunk"):
                                    gs.adjustMomentum(offense, momentumDunkSwing, "made dunk")
                                elif madeShotResult == "paint_poster_dunk":
                                    gs.adjustMomentum(offense, momentumPosterDunkSwing, "poster dunk")
                                else:
                                    gs.adjustMomentum(offense, momentumMadeTwoSwing, "made two-point shot")
                            else:
                                if shotBlocked:
                                    if offense == t1:
                                        gs.t2stats.at[defender["id"].item(), "Blk"] += 1
                                    else:
                                        gs.t1stats.at[defender["id"].item(), "Blk"] += 1
                                    print(
                                        f"...BLOCKED by {defender['position']} {defender['first_name']} {defender['last_name']}!"
                                    )
                                    gs.adjustMomentum(defense, momentumBlockSwing, "blocked two-point shot")
                                elif shootingFoul:
                                    print("...MISSED, but a shooting foul is called!")
                                    gs.adjustMomentum(defense, momentumMissSwing, "missed two-point shot")
                                else:
                                    print("...MISSED!")
                                    gs.adjustMomentum(defense, momentumMissSwing, "missed two-point shot")
                            gs.assistPlayer = None
                            freeThrowsAwarded = 0
                            lastFreeThrowMade = False
                            if shootingFoul:
                                freeThrowsAwarded = 1 if shotMade else 2
                                print(
                                    f"FOUL on {defender['position']} {defender['first_name']} {defender['last_name']}! {shootPlayer['position']} {shootPlayer['first_name']} {shootPlayer['last_name']} will shoot {freeThrowsAwarded} free throw{'s' if freeThrowsAwarded != 1 else ''}."
                                )
                                ftMediaTimeout = gs.checkTimeoutStoppage(offense, True, shootPlayer)
                                ftSubsCompleted = ftMediaTimeout
                                if (defenderFouledOut or defenderFoulProtected) and not ftSubsCompleted:
                                    gs.pullFreeThrowSubs(shootPlayer)
                                    ftSubsCompleted = True
                                    gs.defendedPlayerId = None
                                    gs.currentDefender = None
                                    gs.previousDefender = None
                                elif freeThrowsAwarded == 1 and not ftSubsCompleted:
                                    gs.pullFreeThrowSubs(shootPlayer)
                                    ftSubsCompleted = True
                                if offense == t1:
                                    offense_df = gs.t1onCourt
                                    defense_df = gs.t2onCourt
                                    ftStats = gs.t1stats
                                else:
                                    offense_df = gs.t2onCourt
                                    defense_df = gs.t1onCourt
                                    ftStats = gs.t2stats
                                shootPlayerMinutes = float(ftStats.at[shootPlayer["id"].item(), "MP"]) / 60
                                shootPlayerRecoveryMinutes = gs.getPlayerRecoveryMinutes(shootPlayer)
                                shootPlayerFatigueMinutes = max(0.0, shootPlayerMinutes - shootPlayerRecoveryMinutes)
                                (
                                    _,
                                    _,
                                    shooterStaminaCapacity,
                                    shootPlayerMinutes,
                                    shooterStaminaUsageRatio,
                                    shooterFatiguePenalty,
                                    shooterStaminaModifier,
                                ) = get_stamina_adjusted_rating(
                                    shootPlayer, "free_throw", shootPlayerMinutes, shootPlayerRecoveryMinutes
                                )
                                ftHCA = gs.HCAAdj if offense == t1 else 0
                                for ftNum in range(1, freeThrowsAwarded + 1):
                                    ftMade, ftChance, ftRoll, ftRating, baseFTRating = resolve_free_throw(
                                        shootPlayer, ftHCA, shooterStaminaModifier
                                    )
                                    if offense == t1:
                                        gs.t1stats.at[shootPlayer["id"].item(), "FT Shot Att"] += 1
                                    else:
                                        gs.t2stats.at[shootPlayer["id"].item(), "FT Shot Att"] += 1
                                    if ftMade:
                                        if offense == t1:
                                            gs.t1pts += 1
                                            gs.t1stats.at[shootPlayer["id"].item(), "FT Shot Made"] += 1
                                            if gs.period == 1:
                                                gs.t1q1pts += 1
                                            elif gs.period == 2:
                                                gs.t1q2pts += 1
                                            elif gs.league != "CBB" and gs.period == 3:
                                                gs.t1q3pts += 1
                                            elif gs.league != "CBB" and gs.period == 4:
                                                gs.t1q4pts += 1
                                            elif gs.period > gs.periodPerGame:
                                                gs.t1qotpts += 1
                                        else:
                                            gs.t2pts += 1
                                            gs.t2stats.at[shootPlayer["id"].item(), "FT Shot Made"] += 1
                                            if gs.period == 1:
                                                gs.t2q1pts += 1
                                            elif gs.period == 2:
                                                gs.t2q2pts += 1
                                            elif gs.league != "CBB" and gs.period == 3:
                                                gs.t2q3pts += 1
                                            elif gs.league != "CBB" and gs.period == 4:
                                                gs.t2q4pts += 1
                                            elif gs.period > gs.periodPerGame:
                                                gs.t2qotpts += 1
                                    print(
                                        f"Free throw {ftNum} of {freeThrowsAwarded}: rating {ftRating:.4f} [base {baseFTRating:.2f}; MP {shootPlayerMinutes:.2f}; recovery {shootPlayerRecoveryMinutes:.2f}; fatigue load {shootPlayerFatigueMinutes:.2f}/{shooterStaminaCapacity:.2f}; modifier {shooterStaminaModifier:.3f}] | Chance: {ftChance:.2%} | Roll: {ftRoll:.4f} | {'GOOD' if ftMade else 'MISSED'}"
                                    )
                                    lastFreeThrowMade = ftMade
                                    if ftNum == 1 and freeThrowsAwarded > 1 and not ftSubsCompleted:
                                        gs.pullFreeThrowSubs(shootPlayer)
                                        ftSubsCompleted = True
                                        if offense == t1:
                                            offense_df = gs.t1onCourt
                                            defense_df = gs.t2onCourt
                                        else:
                                            offense_df = gs.t2onCourt
                                            defense_df = gs.t1onCourt
                            needsRebound = (not shootingFoul and not shotMade) or (
                                shootingFoul and not lastFreeThrowMade
                            )
                            if needsRebound:
                                rebRand = random.random()
                                offensiveReboundChance = gs.lineupParameters[
                                    "t1OffensiveRebound" if offense == t1 else "t2OffensiveRebound"
                                ]
                                if rebRand < offensiveReboundChance:
                                    gs.possPlayer = random.choice(list(offense_df.values()))
                                    if offense == t1:
                                        gs.t1stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                    else:
                                        gs.t2stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                    print(
                                        gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " grabs the offensive rebound for "
                                        + gs.possTeam
                                    )
                                    gs.currShotClock = gs.shotClockReset
                                    if gs.currTime < gs.currShotClock:
                                        gs.currShotClock = gs.currTime
                                else:
                                    gs.possPlayer = random.choice(list(defense_df.values()))
                                    if offense == t1:
                                        gs.t2stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                        gs.possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = gs.t2onCourt
                                        defense_df = gs.t1onCourt
                                        gs.courtPos = (random.randint(2, 4), random.randint(2, 4))
                                    else:
                                        gs.t1stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                        gs.possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = gs.t1onCourt
                                        defense_df = gs.t2onCourt
                                        gs.courtPos = (random.randint(2, 4) * -1, random.randint(2, 4))
                                    gs.currShotClock = gs.shotClock
                                    if gs.currTime <= gs.shotClock:
                                        gs.currShotClock = gs.currTime
                                    gs.crossed_midcourt = False
                                    print(
                                        gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " grabs the defensive rebound for "
                                        + gs.possTeam
                                    )
                                    gs.defendedPlayerId = None
                                    gs.currentDefender = None
                                    gs.previousDefender = None
                            else:
                                if offense == t1:
                                    gs.possTeam = t2
                                    offense_df = gs.t2onCourt
                                    defense_df = gs.t1onCourt
                                    gs.courtPos = (4, 3)
                                    gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                                else:
                                    gs.possTeam = t1
                                    offense_df = gs.t1onCourt
                                    defense_df = gs.t2onCourt
                                    gs.courtPos = (-4, 3)
                                    gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                                gs.crossed_midcourt = False
                                gs.currShotClock = gs.shotClock
                                if gs.currTime <= gs.shotClock:
                                    gs.currShotClock = gs.currTime
                                print(
                                    gs.possPlayer["position"]
                                    + " "
                                    + gs.possPlayer["first_name"]
                                    + " "
                                    + gs.possPlayer["last_name"]
                                    + " takes the ball out for "
                                    + gs.possTeam
                                )
                                gs.finalHeavePending = True
                                gs.defendedPlayerId = None
                                gs.currentDefender = None
                                gs.previousDefender = None
                            print(t1 + ": " + str(gs.t1pts) + " / " + t2 + ": " + str(gs.t2pts))
                            print(footerPos)
                            gs.printMomentumMeter()
                            took_shot = True

            if not took_shot:
                if gs.currShotClock <= 0 and action != "shot" and gs.currTime > 0:
                    print("Shot clock violation.")
                    gs.checkTimeoutStoppage(defense, False)
                    gs.assistPlayer = None
                    gs.currShotClock = gs.shotClock
                    if gs.currTime <= gs.shotClock:
                        gs.currShotClock = gs.currTime
                    gs.crossed_midcourt = False
                    if offense == t1:
                        gs.t1stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                        gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                        gs.possTeam = t2
                        offense_df = gs.t2onCourt
                        defense_df = gs.t1onCourt
                        gs.courtPos = (4, 3)
                        print(
                            gs.possPlayer["position"]
                            + " "
                            + gs.possPlayer["first_name"]
                            + " "
                            + gs.possPlayer["last_name"]
                            + " takes over for "
                            + t2
                            + "."
                        )
                    else:
                        gs.t2stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                        gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                        gs.possTeam = t1
                        offense_df = gs.t1onCourt
                        defense_df = gs.t2onCourt
                        gs.courtPos = (-4, 3)
                        print(
                            gs.possPlayer["position"]
                            + " "
                            + gs.possPlayer["first_name"]
                            + " "
                            + gs.possPlayer["last_name"]
                            + " takes over for "
                            + t1
                            + "."
                        )
                    gs.finalHeavePending = True

                else:
                    if action == "move":
                        if gs.assistPlayer is not None:
                            gs.assistMovementCount += 1
                            if gs.assistMovementCount > 1:
                                gs.assistPlayer = None
                                gs.assistMovementCount = 0
                        formationWeights = (
                            gs.t1FormationDestinationWeights if offense == t1 else gs.t2FormationDestinationWeights
                        )
                        activeDestinationWeights, activeLineupPreferences = gs.getActiveDestinationWeights(
                            offense_df, formationWeights
                        )
                        newPos = choose_weighted_move_spot(
                            team_side, gs.courtPos, gs.crossed_midcourt, activeDestinationWeights
                        )
                        if newPos is not None:
                            (
                                offensiveFoulChance,
                                offensiveFoulBaseline,
                                offensivePlayerIQ,
                                offensiveBBIQModifier,
                                offensiveFoulDefenderIQ,
                                offensiveFoulDefenderBBIQModifier,
                            ) = get_offensive_foul_chance(gs.possPlayer, defender, newPos)
                            offensiveFoulRoll = random.random()
                            offensiveFoul = offensiveFoulRoll < offensiveFoulChance
                            print(
                                f"Offensive foul baseline: {offensiveFoulBaseline:.2%} | Offensive BBIQ: {offensivePlayerIQ:.0f} | Offensive modifier: {offensiveBBIQModifier:.3f} | Defender BBIQ: {offensiveFoulDefenderIQ:.0f} | Defender modifier: {offensiveFoulDefenderBBIQModifier:.3f} | Foul chance: {offensiveFoulChance:.2%} | Foul roll: {offensiveFoulRoll:.4f} | {'CHARGE' if offensiveFoul else 'NO OFFENSIVE FOUL'}"
                            )
                            if not offensiveFoul:
                                nonShootingFoulChance, zoneFoulBaseline, foulDefenderIQ, bbiqFoulModifier = (
                                    get_non_shooting_foul_chance(defender, newPos)
                                )
                                nonShootingFoulRoll = random.random()
                                nonShootingFoul = nonShootingFoulRoll < nonShootingFoulChance
                                print(
                                    f"Non-shooting foul baseline: {zoneFoulBaseline:.2%} | Defender BBIQ: {foulDefenderIQ:.0f} | BBIQ modifier: {bbiqFoulModifier:.3f} | Foul chance: {nonShootingFoulChance:.2%} | Foul roll: {nonShootingFoulRoll:.4f} | {'FOUL' if nonShootingFoul else 'NO FOUL'}"
                                )
                                if not nonShootingFoul:
                                    offenseStats = gs.t1stats if offense == t1 else gs.t2stats
                                    defenseStats = gs.t2stats if offense == t1 else gs.t1stats
                                    possPlayerMinutes = float(offenseStats.at[gs.possPlayer["id"].item(), "MP"]) / 60
                                    defenderMinutes = float(defenseStats.at[defender["id"].item(), "MP"]) / 60
                                    possPlayerRecoveryMinutes = gs.getPlayerRecoveryMinutes(gs.possPlayer)
                                    defenderRecoveryMinutes = gs.getPlayerRecoveryMinutes(defender)
                                    possPlayerFatigueMinutes = max(0.0, possPlayerMinutes - possPlayerRecoveryMinutes)
                                    defenderFatigueMinutes = max(0.0, defenderMinutes - defenderRecoveryMinutes)
                                    (
                                        movementOffense,
                                        baseMovementOffense,
                                        offensiveStaminaCapacity,
                                        possPlayerMinutes,
                                        offensiveStaminaUsageRatio,
                                        offensiveFatiguePenalty,
                                        offensiveStaminaModifier,
                                    ) = get_stamina_adjusted_rating(
                                        gs.possPlayer, "agility", possPlayerMinutes, possPlayerRecoveryMinutes
                                    )
                                    movementOffenseType = "agility"
                                    staminaAdjustedMovementOffense = movementOffense
                                    (
                                        movementOffense,
                                        movementMomentumStrength,
                                        movementMomentumBonus,
                                        movementMomentumModifier,
                                    ) = gs.getMomentumAdjustedRating(staminaAdjustedMovementOffense, offense)
                                    (
                                        _,
                                        _,
                                        defenderStaminaCapacity,
                                        defenderMinutes,
                                        defenderStaminaUsageRatio,
                                        defenderFatiguePenalty,
                                        defenderStaminaModifier,
                                    ) = get_stamina_adjusted_rating(
                                        defender, "perimeter_defense", defenderMinutes, defenderRecoveryMinutes
                                    )
                                    baseMovementDefense, movementDefenseType = get_movement_defense(defender, newPos)
                                    movementDefense, movementDefenseType = get_movement_defense(
                                        defender, newPos, defenderStaminaModifier
                                    )
                                    movementSuccessProbability = max(
                                        0.10,
                                        min(
                                            0.90,
                                            get_movement_success_probability(movementOffense, movementDefense)
                                            + doubleTeamMovementAdjustment,
                                        ),
                                    )
                                    movementRoll = random.random()
                                    movementSuccessful = movementRoll < movementSuccessProbability
                                    print(
                                        f"Movement offense: {movementOffense:.4f} [{movementOffenseType}; base {baseMovementOffense:.2f}; stamina adjusted {staminaAdjustedMovementOffense:.4f}; MP {possPlayerMinutes:.2f}; recovery {possPlayerRecoveryMinutes:.2f}; fatigue load {possPlayerFatigueMinutes:.2f}/{offensiveStaminaCapacity:.2f}; stamina modifier {offensiveStaminaModifier:.3f}; momentum {movementMomentumStrength:.0%}; momentum bonus {movementMomentumBonus:.2%}; momentum modifier {movementMomentumModifier:.3f}] | Movement defense: {movementDefense:.4f} [{movementDefenseType}; base {baseMovementDefense:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Double-team role: {doubleTeamRole} {doubleTeamMovementAdjustment:+.2%} | Success chance: {movementSuccessProbability:.2%} | Roll: {movementRoll:.4f} | {'SUCCESS' if movementSuccessful else 'CUT OFF'} at {format_court_pos(newPos)}"
                                    )
                                    if movementSuccessful:
                                        gs.courtPos = newPos
                                        gs.crossed_midcourt = update_crossed_midcourt(
                                            team_side, gs.courtPos, gs.crossed_midcourt
                                        )
                                    print(
                                        periodLabel
                                        + ": "
                                        + game_clock_text
                                        + " / Shot Clock: :"
                                        + shot_clock_text
                                        + " ("
                                        + gs.possTeam
                                        + ")"
                                    )
                                    if movementSuccessful:
                                        print(
                                            gs.possPlayer["position"]
                                            + " "
                                            + gs.possPlayer["first_name"]
                                            + " "
                                            + gs.possPlayer["last_name"]
                                            + " moves the ball up the court for "
                                            + gs.possTeam
                                            + "."
                                        )
                                    else:
                                        print(
                                            gs.possPlayer["position"]
                                            + " "
                                            + gs.possPlayer["first_name"]
                                            + " "
                                            + gs.possPlayer["last_name"]
                                            + " is cut off and remains at "
                                            + format_court_pos(gs.courtPos)
                                            + "."
                                        )
                                    print(footerPos)
                                    gs.printMomentumMeter()
                                else:
                                    gs.assistPlayer = None
                                    gs.assistMovementCount = 0
                                    defenderFouledOut = False
                                    defenderFoulProtected = False
                                    defenderStatId = defender["id"].item()
                                    defenderPlayerId = int(defender["ID"])
                                    if offense == t1:
                                        gs.t2stats.at[defenderStatId, "Foul"] += 1
                                        if gs.period == 1:
                                            gs.t2FirstHalfTeamFouls += 1
                                            defendingHalfTeamFouls = gs.t2FirstHalfTeamFouls
                                        else:
                                            gs.t2SecondHalfTeamFouls += 1
                                            defendingHalfTeamFouls = gs.t2SecondHalfTeamFouls
                                        defenderFoulTotal = int(gs.t2stats.at[defenderStatId, "Foul"])
                                        if (
                                            defenderFoulTotal >= gs.foulOutLimit
                                            and defenderPlayerId not in gs.t2FouledOutPlayerIds
                                        ):
                                            gs.t2FouledOutPlayerIds.add(defenderPlayerId)
                                            defenderFouledOut = True
                                        defenderFoulProtected = gs.registerFoulProtection(
                                            2,
                                            defenderStatId,
                                            defenderPlayerId,
                                            f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                        )
                                    else:
                                        gs.t1stats.at[defenderStatId, "Foul"] += 1
                                        if gs.period == 1:
                                            gs.t1FirstHalfTeamFouls += 1
                                            defendingHalfTeamFouls = gs.t1FirstHalfTeamFouls
                                        else:
                                            gs.t1SecondHalfTeamFouls += 1
                                            defendingHalfTeamFouls = gs.t1SecondHalfTeamFouls
                                        defenderFoulTotal = int(gs.t1stats.at[defenderStatId, "Foul"])
                                        if (
                                            defenderFoulTotal >= gs.foulOutLimit
                                            and defenderPlayerId not in gs.t1FouledOutPlayerIds
                                        ):
                                            gs.t1FouledOutPlayerIds.add(defenderPlayerId)
                                            defenderFouledOut = True
                                        defenderFoulProtected = gs.registerFoulProtection(
                                            1,
                                            defenderStatId,
                                            defenderPlayerId,
                                            f"{defender['position']} {defender['first_name']} {defender['last_name']}",
                                        )
                                    if gs.league == "CBB" and defendingHalfTeamFouls >= 10:
                                        bonusType = "double_bonus"
                                    elif gs.league == "CBB" and defendingHalfTeamFouls >= 7:
                                        bonusType = "one_and_one"
                                    else:
                                        bonusType = None
                                    print(
                                        periodLabel
                                        + ": "
                                        + game_clock_text
                                        + " / Shot Clock: :"
                                        + shot_clock_text
                                        + " ("
                                        + gs.possTeam
                                        + ")"
                                    )
                                    print(
                                        f"Non-shooting foul by {defender['position']} {defender['first_name']} {defender['last_name']} on {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']}!"
                                    )
                                    print(f"Defending team fouls this half: {defendingHalfTeamFouls}")
                                    if defenderFouledOut:
                                        print(
                                            f"{defender['position']} {defender['first_name']} {defender['last_name']} has fouled out with {defenderFoulTotal} fouls!"
                                        )
                                    freeThrowsAwarded = 0
                                    lastFreeThrowMade = False
                                    if bonusType == "one_and_one":
                                        freeThrowsAwarded = 2
                                        print(
                                            f"{gs.possTeam} is in the bonus. {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} will shoot one-and-one."
                                        )
                                    elif bonusType == "double_bonus":
                                        freeThrowsAwarded = 2
                                        print(
                                            f"{gs.possTeam} is in the double bonus. {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} will shoot two free throws."
                                        )
                                    protectedFTPlayer = gs.possPlayer if freeThrowsAwarded > 0 else None
                                    nsFoulMediaTimeout = gs.checkTimeoutStoppage(offense, True, protectedFTPlayer)
                                    ftSubsCompleted = nsFoulMediaTimeout
                                    if (
                                        (defenderFouledOut or defenderFoulProtected)
                                        and freeThrowsAwarded > 0
                                        and not ftSubsCompleted
                                    ):
                                        gs.pullFreeThrowSubs(gs.possPlayer)
                                        ftSubsCompleted = True
                                        gs.defendedPlayerId = None
                                        gs.currentDefender = None
                                        gs.previousDefender = None
                                    if offense == t1:
                                        offense_df = gs.t1onCourt
                                        defense_df = gs.t2onCourt
                                        ftStats = gs.t1stats
                                    else:
                                        offense_df = gs.t2onCourt
                                        defense_df = gs.t1onCourt
                                        ftStats = gs.t2stats
                                    if freeThrowsAwarded > 0:
                                        ftHCA = gs.HCAAdj if offense == t1 else 0
                                        ftShooterMinutes = float(ftStats.at[gs.possPlayer["id"].item(), "MP"]) / 60
                                        ftRecoveryMinutes = gs.getPlayerRecoveryMinutes(gs.possPlayer)
                                        ftFatigueMinutes = max(0.0, ftShooterMinutes - ftRecoveryMinutes)
                                        (
                                            _,
                                            _,
                                            ftStaminaCapacity,
                                            ftShooterMinutes,
                                            ftStaminaUsageRatio,
                                            ftFatiguePenalty,
                                            ftStaminaModifier,
                                        ) = get_stamina_adjusted_rating(
                                            gs.possPlayer, "free_throw", ftShooterMinutes, ftRecoveryMinutes
                                        )
                                        for ftNum in range(1, freeThrowsAwarded + 1):
                                            ftMade, ftChance, ftRoll, ftRating, baseFTRating = resolve_free_throw(
                                                gs.possPlayer, ftHCA, ftStaminaModifier
                                            )
                                            if offense == t1:
                                                gs.t1stats.at[gs.possPlayer["id"].item(), "FT Shot Att"] += 1
                                            else:
                                                gs.t2stats.at[gs.possPlayer["id"].item(), "FT Shot Att"] += 1
                                            if ftMade:
                                                if offense == t1:
                                                    gs.t1pts += 1
                                                    gs.t1stats.at[gs.possPlayer["id"].item(), "FT Shot Made"] += 1
                                                    if gs.period == 1:
                                                        gs.t1q1pts += 1
                                                    elif gs.period == 2:
                                                        gs.t1q2pts += 1
                                                    elif gs.league != "CBB" and gs.period == 3:
                                                        gs.t1q3pts += 1
                                                    elif gs.league != "CBB" and gs.period == 4:
                                                        gs.t1q4pts += 1
                                                    elif gs.period > gs.periodPerGame:
                                                        gs.t1qotpts += 1
                                                else:
                                                    gs.t2pts += 1
                                                    gs.t2stats.at[gs.possPlayer["id"].item(), "FT Shot Made"] += 1
                                                    if gs.period == 1:
                                                        gs.t2q1pts += 1
                                                    elif gs.period == 2:
                                                        gs.t2q2pts += 1
                                                    elif gs.league != "CBB" and gs.period == 3:
                                                        gs.t2q3pts += 1
                                                    elif gs.league != "CBB" and gs.period == 4:
                                                        gs.t2q4pts += 1
                                                    elif gs.period > gs.periodPerGame:
                                                        gs.t2qotpts += 1
                                            print(
                                                f"Free throw {ftNum} of {freeThrowsAwarded}: rating {ftRating:.4f} [base {baseFTRating:.2f}; MP {ftShooterMinutes:.2f}; recovery {ftRecoveryMinutes:.2f}; fatigue load {ftFatigueMinutes:.2f}/{ftStaminaCapacity:.2f}; modifier {ftStaminaModifier:.3f}] | Chance: {ftChance:.2%} | Roll: {ftRoll:.4f} | {'GOOD' if ftMade else 'MISSED'}"
                                            )
                                            lastFreeThrowMade = ftMade
                                            if bonusType == "one_and_one" and ftNum == 1 and not ftMade:
                                                print("The front end of the one-and-one is missed. The ball is live!")
                                                break
                                            if ftNum == 1 and freeThrowsAwarded > 1 and not ftSubsCompleted:
                                                gs.pullFreeThrowSubs(gs.possPlayer)
                                                ftSubsCompleted = True
                                                if offense == t1:
                                                    offense_df = gs.t1onCourt
                                                    defense_df = gs.t2onCourt
                                                else:
                                                    offense_df = gs.t2onCourt
                                                    defense_df = gs.t1onCourt
                                    if (
                                        (defenderFouledOut or defenderFoulProtected)
                                        and freeThrowsAwarded == 0
                                        and not nsFoulMediaTimeout
                                    ):
                                        gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(False)
                                        if offense == t1:
                                            offense_df = gs.t1onCourt
                                            defense_df = gs.t2onCourt
                                        else:
                                            offense_df = gs.t2onCourt
                                            defense_df = gs.t1onCourt
                                        gs.defendedPlayerId = None
                                        gs.currentDefender = None
                                        gs.previousDefender = None
                                        subReason = "foul-out" if defenderFouledOut else "foul protection"
                                        print(t1 + " Subs after " + subReason + ":")
                                        for p in gs.t1onCourt.values():
                                            print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                                        print(t2 + " Subs after " + subReason + ":")
                                        for p in gs.t2onCourt.values():
                                            print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                                    if bonusType is None:
                                        gs.possPlayer = random.choice(list(offense_df.values()))
                                        gs.currShotClock = max(gs.currShotClock, gs.shotClockReset)
                                        if gs.currTime < gs.currShotClock:
                                            gs.currShotClock = gs.currTime
                                        gs.defendedPlayerId = None
                                        gs.currentDefender = None
                                        gs.previousDefender = None
                                        print(
                                            gs.possPlayer["position"]
                                            + " "
                                            + gs.possPlayer["first_name"]
                                            + " "
                                            + gs.possPlayer["last_name"]
                                            + " takes the ball out for "
                                            + gs.possTeam
                                            + "."
                                        )
                                        gs.finalHeavePending = True
                                    elif not lastFreeThrowMade:
                                        rebRand = random.random()
                                        offensiveReboundChance = gs.lineupParameters[
                                            "t1OffensiveRebound" if offense == t1 else "t2OffensiveRebound"
                                        ]
                                        if rebRand < offensiveReboundChance:
                                            gs.possPlayer = random.choice(list(offense_df.values()))
                                            if offense == t1:
                                                gs.t1stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                            else:
                                                gs.t2stats.at[gs.possPlayer["id"].item(), "OREB"] += 1
                                            print(
                                                gs.possPlayer["position"]
                                                + " "
                                                + gs.possPlayer["first_name"]
                                                + " "
                                                + gs.possPlayer["last_name"]
                                                + " grabs the offensive rebound for "
                                                + gs.possTeam
                                            )
                                            gs.currShotClock = gs.shotClockReset
                                            if gs.currTime < gs.currShotClock:
                                                gs.currShotClock = gs.currTime
                                        else:
                                            gs.possPlayer = random.choice(list(defense_df.values()))
                                            if offense == t1:
                                                gs.t2stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                                gs.possTeam = t2
                                                offense = t2
                                                defense = t1
                                                offense_df = gs.t2onCourt
                                                defense_df = gs.t1onCourt
                                                gs.courtPos = (random.randint(2, 4), random.randint(2, 4))
                                            else:
                                                gs.t1stats.at[gs.possPlayer["id"].item(), "DREB"] += 1
                                                gs.possTeam = t1
                                                offense = t1
                                                defense = t2
                                                offense_df = gs.t1onCourt
                                                defense_df = gs.t2onCourt
                                                gs.courtPos = (random.randint(2, 4) * -1, random.randint(2, 4))
                                            gs.currShotClock = gs.shotClock
                                            if gs.currTime <= gs.shotClock:
                                                gs.currShotClock = gs.currTime
                                            gs.crossed_midcourt = False
                                            print(
                                                gs.possPlayer["position"]
                                                + " "
                                                + gs.possPlayer["first_name"]
                                                + " "
                                                + gs.possPlayer["last_name"]
                                                + " grabs the defensive rebound for "
                                                + gs.possTeam
                                            )
                                            gs.defendedPlayerId = None
                                            gs.currentDefender = None
                                            gs.previousDefender = None
                                    else:
                                        if offense == t1:
                                            gs.possTeam = t2
                                            offense_df = gs.t2onCourt
                                            defense_df = gs.t1onCourt
                                            gs.courtPos = (4, 3)
                                            gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                                        else:
                                            gs.possTeam = t1
                                            offense_df = gs.t1onCourt
                                            defense_df = gs.t2onCourt
                                            gs.courtPos = (-4, 3)
                                            gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                                        gs.crossed_midcourt = False
                                        gs.currShotClock = gs.shotClock
                                        if gs.currTime <= gs.shotClock:
                                            gs.currShotClock = gs.currTime
                                        gs.defendedPlayerId = None
                                        gs.currentDefender = None
                                        gs.previousDefender = None
                                        print(
                                            gs.possPlayer["position"]
                                            + " "
                                            + gs.possPlayer["first_name"]
                                            + " "
                                            + gs.possPlayer["last_name"]
                                            + " takes the ball out for "
                                            + gs.possTeam
                                        )
                                        gs.finalHeavePending = True
                                    print(footerPos)
                                    gs.printMomentumMeter()
                            else:
                                gs.assistPlayer = None
                                gs.assistMovementCount = 0
                                offensivePlayerFouledOut = False
                                offensivePlayerFoulProtected = False
                                offensivePlayerStatId = gs.possPlayer["id"].item()
                                offensivePlayerId = int(gs.possPlayer["ID"])
                                if offense == t1:
                                    gs.t1stats.at[offensivePlayerStatId, "Foul"] += 1
                                    gs.t1stats.at[offensivePlayerStatId, "TO"] += 1
                                    if gs.period == 1:
                                        gs.t1FirstHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = gs.t1FirstHalfTeamFouls
                                    else:
                                        gs.t1SecondHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = gs.t1SecondHalfTeamFouls
                                    offensivePlayerFoulTotal = int(gs.t1stats.at[offensivePlayerStatId, "Foul"])
                                    if (
                                        offensivePlayerFoulTotal >= gs.foulOutLimit
                                        and offensivePlayerId not in gs.t1FouledOutPlayerIds
                                    ):
                                        gs.t1FouledOutPlayerIds.add(offensivePlayerId)
                                        offensivePlayerFouledOut = True
                                    offensivePlayerFoulProtected = gs.registerFoulProtection(
                                        1,
                                        offensivePlayerStatId,
                                        offensivePlayerId,
                                        f"{gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']}",
                                    )
                                else:
                                    gs.t2stats.at[offensivePlayerStatId, "Foul"] += 1
                                    gs.t2stats.at[offensivePlayerStatId, "TO"] += 1
                                    if gs.period == 1:
                                        gs.t2FirstHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = gs.t2FirstHalfTeamFouls
                                    else:
                                        gs.t2SecondHalfTeamFouls += 1
                                        offensiveHalfTeamFouls = gs.t2SecondHalfTeamFouls
                                    offensivePlayerFoulTotal = int(gs.t2stats.at[offensivePlayerStatId, "Foul"])
                                    if (
                                        offensivePlayerFoulTotal >= gs.foulOutLimit
                                        and offensivePlayerId not in gs.t2FouledOutPlayerIds
                                    ):
                                        gs.t2FouledOutPlayerIds.add(offensivePlayerId)
                                        offensivePlayerFouledOut = True
                                    offensivePlayerFoulProtected = gs.registerFoulProtection(
                                        2,
                                        offensivePlayerStatId,
                                        offensivePlayerId,
                                        f"{gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']}",
                                    )
                                print(
                                    periodLabel
                                    + ": "
                                    + game_clock_text
                                    + " / Shot Clock: :"
                                    + shot_clock_text
                                    + " ("
                                    + gs.possTeam
                                    + ")"
                                )
                                print(
                                    f"OFFENSIVE FOUL! {gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} is called for a charge drawn by {defender['position']} {defender['first_name']} {defender['last_name']}!"
                                )
                                print(f"Offensive team fouls this half: {offensiveHalfTeamFouls}")
                                if offensivePlayerFouledOut:
                                    print(
                                        f"{gs.possPlayer['position']} {gs.possPlayer['first_name']} {gs.possPlayer['last_name']} has fouled out with {offensivePlayerFoulTotal} fouls!"
                                    )
                                offFoulMediaTimeout = gs.checkTimeoutStoppage(defense, True)
                                if (
                                    offensivePlayerFouledOut or offensivePlayerFoulProtected
                                ) and not offFoulMediaTimeout:
                                    gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(False)
                                    subReason = "foul-out" if offensivePlayerFouledOut else "foul protection"
                                    print(t1 + " Subs after " + subReason + ":")
                                    for p in gs.t1onCourt.values():
                                        print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                                    print(t2 + " Subs after " + subReason + ":")
                                    for p in gs.t2onCourt.values():
                                        print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                                if offense == t1:
                                    gs.possTeam = t2
                                    offense_df = gs.t2onCourt
                                    defense_df = gs.t1onCourt
                                    gs.courtPos = (4, 3)
                                    gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                                else:
                                    gs.possTeam = t1
                                    offense_df = gs.t1onCourt
                                    defense_df = gs.t2onCourt
                                    gs.courtPos = (-4, 3)
                                    gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                                gs.crossed_midcourt = False
                                gs.currShotClock = gs.shotClock
                                if gs.currTime <= gs.shotClock:
                                    gs.currShotClock = gs.currTime
                                gs.assistPlayer = None
                                gs.defendedPlayerId = None
                                gs.currentDefender = None
                                gs.previousDefender = None
                                print(
                                    gs.possPlayer["position"]
                                    + " "
                                    + gs.possPlayer["first_name"]
                                    + " "
                                    + gs.possPlayer["last_name"]
                                    + " takes the ball out for "
                                    + gs.possTeam
                                    + "."
                                )
                                gs.finalHeavePending = True
                                print(footerPos)
                                gs.printMomentumMeter()
                        else:
                            print(
                                periodLabel
                                + ": "
                                + game_clock_text
                                + " / Shot Clock: :"
                                + shot_clock_text
                                + " ("
                                + gs.possTeam
                                + ")"
                            )
                            print(
                                gs.possPlayer["position"]
                                + " "
                                + gs.possPlayer["first_name"]
                                + " "
                                + gs.possPlayer["last_name"]
                                + " is trapped and cannot move."
                            )
                            print(footerPos)
                            gs.printMomentumMeter()

                    elif action == "pass":
                        formationWeights = (
                            gs.t1FormationDestinationWeights if offense == t1 else gs.t2FormationDestinationWeights
                        )
                        activeDestinationWeights, activeLineupPreferences = gs.getActiveDestinationWeights(
                            offense_df, formationWeights
                        )
                        targetPos = choose_weighted_pass_target(
                            team_side, gs.courtPos, gs.crossed_midcourt, activeDestinationWeights
                        )
                        if targetPos is not None:
                            offenseStats = gs.t1stats if offense == t1 else gs.t2stats
                            defenseStats = gs.t2stats if offense == t1 else gs.t1stats
                            possPlayerMinutes = float(offenseStats.at[gs.possPlayer["id"].item(), "MP"]) / 60
                            defenderMinutes = float(defenseStats.at[defender["id"].item(), "MP"]) / 60
                            possPlayerRecoveryMinutes = gs.getPlayerRecoveryMinutes(gs.possPlayer)
                            defenderRecoveryMinutes = gs.getPlayerRecoveryMinutes(defender)
                            possPlayerFatigueMinutes = max(0.0, possPlayerMinutes - possPlayerRecoveryMinutes)
                            defenderFatigueMinutes = max(0.0, defenderMinutes - defenderRecoveryMinutes)
                            (
                                passOffense,
                                basePassOffense,
                                offensiveStaminaCapacity,
                                possPlayerMinutes,
                                offensiveStaminaUsageRatio,
                                offensiveFatiguePenalty,
                                offensiveStaminaModifier,
                            ) = get_stamina_adjusted_rating(
                                gs.possPlayer, "ballwork", possPlayerMinutes, possPlayerRecoveryMinutes
                            )
                            passOffenseType = "ballwork"
                            staminaAdjustedPassOffense = passOffense
                            passOffense, passMomentumStrength, passMomentumBonus, passMomentumModifier = (
                                gs.getMomentumAdjustedRating(staminaAdjustedPassOffense, offense)
                            )
                            (
                                _,
                                _,
                                defenderStaminaCapacity,
                                defenderMinutes,
                                defenderStaminaUsageRatio,
                                defenderFatiguePenalty,
                                defenderStaminaModifier,
                            ) = get_stamina_adjusted_rating(
                                defender, "perimeter_defense", defenderMinutes, defenderRecoveryMinutes
                            )
                            basePassDefense, passDefenseType = get_movement_defense(defender, gs.courtPos)
                            passDefense, passDefenseType = get_movement_defense(
                                defender, gs.courtPos, defenderStaminaModifier
                            )
                            distanceDeflectionChance = get_pass_turnover_chance(gs.courtPos, targetPos)
                            passDeflectionChance = max(
                                passDeflectionMinimum,
                                min(
                                    passDeflectionMaximum,
                                    get_pass_deflection_chance(gs.courtPos, targetPos, passOffense, passDefense)
                                    + doubleTeamPassDeflectionAdjustment,
                                ),
                            )
                            passRoll = random.random()
                            passDeflected = passRoll < passDeflectionChance
                            print(
                                f"Pass offense: {passOffense:.4f} [{passOffenseType}; base {basePassOffense:.2f}; stamina adjusted {staminaAdjustedPassOffense:.4f}; MP {possPlayerMinutes:.2f}; recovery {possPlayerRecoveryMinutes:.2f}; fatigue load {possPlayerFatigueMinutes:.2f}/{offensiveStaminaCapacity:.2f}; stamina modifier {offensiveStaminaModifier:.3f}; momentum {passMomentumStrength:.0%}; momentum bonus {passMomentumBonus:.2%}; momentum modifier {passMomentumModifier:.3f}] | Pass defense: {passDefense:.4f} [{passDefenseType}; base {basePassDefense:.2f}; MP {defenderMinutes:.2f}; recovery {defenderRecoveryMinutes:.2f}; fatigue load {defenderFatigueMinutes:.2f}/{defenderStaminaCapacity:.2f}; stamina modifier {defenderStaminaModifier:.3f}] | Distance chance: {distanceDeflectionChance:.2%} | Double-team role: {doubleTeamRole} {doubleTeamPassDeflectionAdjustment:+.2%} | Final deflection chance: {passDeflectionChance:.2%} | Roll: {passRoll:.4f} | {'DEFLECTED' if passDeflected else 'CLEAN'} toward {format_court_pos(targetPos)}"
                            )
                            if passDeflected:
                                looseRand = random.random()
                                looseBallCO = gs.lineupParameters["t1LooseBall" if gs.possTeam == t1 else "t2LooseBall"]
                                if looseRand < looseBallCO:
                                    pickupPlayer = random.choice(list(offense_df.values()))
                                    print(
                                        "Pass from "
                                        + gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " toward "
                                        + format_court_pos(targetPos)
                                        + " is deflected! His teammate "
                                        + pickupPlayer["position"]
                                        + " "
                                        + pickupPlayer["first_name"]
                                        + " "
                                        + pickupPlayer["last_name"]
                                        + " recovers it."
                                    )
                                    print(
                                        periodLabel
                                        + ": "
                                        + game_clock_text
                                        + " / Shot Clock: :"
                                        + shot_clock_text
                                        + " ("
                                        + gs.possTeam
                                        + ")"
                                    )
                                    print(footerPos)
                                    gs.printMomentumMeter()
                                    gs.possPlayer = pickupPlayer
                                    gs.assistPlayer = None
                                else:
                                    pickupPlayer = random.choice(list(defense_df.values()))
                                    print(
                                        "Pass from "
                                        + gs.possPlayer["position"]
                                        + " "
                                        + gs.possPlayer["first_name"]
                                        + " "
                                        + gs.possPlayer["last_name"]
                                        + " toward "
                                        + format_court_pos(targetPos)
                                        + " is deflected! It's recovered by "
                                        + pickupPlayer["position"]
                                        + " "
                                        + pickupPlayer["first_name"]
                                        + " "
                                        + pickupPlayer["last_name"]
                                        + " for "
                                        + defense
                                    )
                                    gs.currShotClock = gs.shotClock
                                    if gs.currTime <= gs.shotClock:
                                        gs.currShotClock = gs.currTime
                                    gs.crossed_midcourt = False
                                    if gs.possTeam == t1:
                                        gs.t1stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                                        gs.t2stats.at[pickupPlayer['id'].item(), 'Stl'] += 1
                                        gs.possTeam = t2
                                        offense = t2
                                        defense = t1
                                        offense_df = gs.t2onCourt
                                        defense_df = gs.t1onCourt
                                    else:
                                        gs.t2stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                                        gs.t1stats.at[pickupPlayer['id'].item(), 'Stl'] += 1
                                        gs.possTeam = t1
                                        offense = t1
                                        defense = t2
                                        offense_df = gs.t1onCourt
                                        defense_df = gs.t2onCourt
                                    gs.defendedPlayerId = None
                                    gs.currentDefender = None
                                    gs.previousDefender = None
                                    gs.possPlayer = pickupPlayer
                                    gs.assistPlayer = None
                            else:
                                gs.assistPlayer = gs.possPlayer
                                gs.assistMovementCount = 0
                                eligiblePassReceivers = [
                                    p for p in offense_df.values() if int(p["id"]) != int(gs.possPlayer["id"])
                                ]
                                passTargetPrefZone = gs.getPreferenceZone(get_shot_zone(targetPos))
                                if passTargetPrefZone is not None:
                                    ptpCol = {
                                        "inside": "inside_preference",
                                        "midrange": "midrange_preference",
                                        "three": "three_preference",
                                    }[passTargetPrefZone]
                                    passReceiverWeights = [
                                        max(
                                            gs.passReceiverPreferenceMinimumWeight,
                                            min(
                                                gs.passReceiverPreferenceMaximumWeight,
                                                1.0
                                                + (
                                                    (float(p[ptpCol]) - activeLineupPreferences[passTargetPrefZone])
                                                    * gs.passReceiverPreferenceWeightPerProportionPoint
                                                ),
                                            ),
                                        )
                                        for p in eligiblePassReceivers
                                    ]
                                    passReceiverIndex = random.choices(
                                        range(len(eligiblePassReceivers)), weights=passReceiverWeights, k=1
                                    )[0]
                                    passReceive = eligiblePassReceivers[passReceiverIndex]
                                    print(
                                        f"Pass receiver preference: {passTargetPrefZone} | Selected: {passReceive['first_name']} {passReceive['last_name']} {float(passReceive[ptpCol]):.1f}% | Active lineup: {activeLineupPreferences[passTargetPrefZone]:.1f}% | Selection weight: {passReceiverWeights[passReceiverIndex]:.3f}"
                                    )
                                else:
                                    passReceive = random.choice(eligiblePassReceivers)
                                gs.courtPos = targetPos
                                gs.crossed_midcourt = update_crossed_midcourt(
                                    team_side, gs.courtPos, gs.crossed_midcourt
                                )
                                print(
                                    periodLabel
                                    + ": "
                                    + game_clock_text
                                    + " / Shot Clock: :"
                                    + shot_clock_text
                                    + " ("
                                    + gs.possTeam
                                    + ")"
                                )
                                print(
                                    gs.possPlayer["position"]
                                    + " "
                                    + gs.possPlayer["first_name"]
                                    + " "
                                    + gs.possPlayer["last_name"]
                                    + " passes the ball to "
                                    + passReceive["position"]
                                    + " "
                                    + passReceive["first_name"]
                                    + " "
                                    + passReceive["last_name"]
                                    + "."
                                )
                                print(footerPos)
                                gs.printMomentumMeter()
                                gs.possPlayer = passReceive
                        else:
                            gs.assistPlayer = None
                            print(
                                periodLabel
                                + ": "
                                + game_clock_text
                                + " / Shot Clock: :"
                                + shot_clock_text
                                + " ("
                                + gs.possTeam
                                + ")"
                            )
                            print(
                                gs.possPlayer["position"]
                                + " "
                                + gs.possPlayer["first_name"]
                                + " "
                                + gs.possPlayer["last_name"]
                                + " has no legal passing lane."
                            )
                            print(footerPos)
                            gs.printMomentumMeter()

                    elif action == "turnover":
                        gs.assistPlayer = None
                        turnoverTeam = gs.possTeam
                        if turnoverTeam == t1:
                            gs.t1stats.at[gs.possPlayer["id"].item(), "TO"] += 1
                        else:
                            gs.t2stats.at[gs.possPlayer["id"].item(), "TO"] += 1
                        print(
                            periodLabel
                            + ": "
                            + game_clock_text
                            + " / Shot Clock: :"
                            + shot_clock_text
                            + " ("
                            + gs.possTeam
                            + ")"
                        )
                        print(
                            gs.possPlayer["position"]
                            + " "
                            + gs.possPlayer["first_name"]
                            + " "
                            + gs.possPlayer["last_name"]
                            + " loses the ball out of bounds."
                        )
                        mediaTimeoutTaken = gs.checkTimeoutStoppage(defense, True)
                        if not mediaTimeoutTaken:
                            gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(False)
                            print(t1 + " Subs:")
                            for p in gs.t1onCourt.values():
                                print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                            print(t2 + " Subs:")
                            for p in gs.t2onCourt.values():
                                print(p["position"] + " " + p["first_name"] + " " + p["last_name"])
                        offense_df = gs.t2onCourt if turnoverTeam == t1 else gs.t1onCourt
                        defense_df = gs.t1onCourt if turnoverTeam == t1 else gs.t2onCourt
                        toTakeout = random.choice(list(offense_df.values()))
                        print(
                            toTakeout["position"]
                            + " "
                            + toTakeout["first_name"]
                            + " "
                            + toTakeout["last_name"]
                            + " will take the ball out for "
                            + defense
                            + "."
                        )
                        gs.finalHeavePending = True
                        print(footerPos)
                        gs.printMomentumMeter()
                        gs.currShotClock = gs.shotClock
                        if gs.currTime <= gs.shotClock:
                            gs.currShotClock = gs.currTime
                        gs.possPlayer = toTakeout
                        gs.defendedPlayerId = None
                        gs.currentDefender = None
                        gs.previousDefender = None
                        if turnoverTeam == t1:
                            gs.possTeam = t2
                            gs.courtPos = (-2, 1) if not gs.crossed_midcourt else (2, 1)
                        else:
                            gs.possTeam = t1
                            gs.courtPos = (2, 1) if not gs.crossed_midcourt else (-2, 1)

                    elif action == "steal":
                        gs.assistPlayer = None
                        stealPlayer = random.choice(list(defense_df.values()))
                        print(
                            periodLabel
                            + ": "
                            + game_clock_text
                            + " / Shot Clock: :"
                            + shot_clock_text
                            + " ("
                            + gs.possTeam
                            + ")"
                        )
                        print(
                            stealPlayer["position"]
                            + " "
                            + stealPlayer["first_name"]
                            + " "
                            + stealPlayer["last_name"]
                            + " picks the ball away for "
                            + defense
                            + "!"
                        )
                        gs.adjustMomentum(defense, momentumStealSwing, "steal")
                        print(footerPos)
                        gs.printMomentumMeter()
                        if gs.possTeam == t1:
                            gs.t1stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                            gs.t2stats.at[stealPlayer['id'].item(), 'Stl'] += 1
                            gs.possTeam = t2
                            offense_df = gs.t2onCourt
                            defense_df = gs.t1onCourt
                        else:
                            gs.t2stats.at[gs.possPlayer['id'].item(), 'TO'] += 1
                            gs.t1stats.at[stealPlayer['id'].item(), 'Stl'] += 1
                            gs.possTeam = t1
                            offense_df = gs.t1onCourt
                            defense_df = gs.t2onCourt
                        gs.defendedPlayerId = None
                        gs.currentDefender = None
                        gs.previousDefender = None
                        gs.possPlayer = stealPlayer
                        gs.currShotClock = gs.shotClock
                        if gs.currTime <= gs.shotClock:
                            gs.currShotClock = gs.currTime
                        gs.crossed_midcourt = False

        if gs.currTime <= 0 and gs.gameOn:
            gs.periodOn = False
            gs.assistPlayer = None
            if gs.period < gs.periodPerGame:
                print(
                    "End of "
                    + ("Half " if gs.league == "CBB" else "Quarter ")
                    + str(gs.period)
                    + ".\n"
                    + t1
                    + ": "
                    + str(gs.t1pts)
                    + " / "
                    + t2
                    + ": "
                    + str(gs.t2pts)
                )
                gs.period += 1
                gs.lastCountedPossessionTeam = None
                if (gs.league == "CBB" and gs.period == 2) or (gs.league != "CBB" and gs.period == 3):
                    gs.t1FoulProtectionBench.clear()
                    gs.t2FoulProtectionBench.clear()
                    gs.t1PlayerHalfFouls.clear()
                    gs.t2PlayerHalfFouls.clear()
                    print("Halftime: all foul-protection restrictions have been cleared.")
                if gs.league == "CBB":
                    gs.applyFatigueRecovery(halftimeRecoveryMinutes, "Halftime breather")
                    gs.dampenMomentum(momentumHalftimeRetention, "halftime")
                elif gs.period == 3:
                    gs.applyFatigueRecovery(halftimeRecoveryMinutes, "Halftime breather")
                    gs.dampenMomentum(momentumHalftimeRetention, "halftime")
                else:
                    gs.applyFatigueRecovery(quarterBreakRecoveryMinutes, "Quarter-break breather")
                    gs.dampenMomentum(momentumQuarterBreakRetention, "quarter break")
                if (gs.league == "CBB" and gs.period == 2) or (gs.league != "CBB" and gs.period == 3):
                    gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(True)
                else:
                    gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(False)
                print(t1 + " Subs:")
                for p in gs.t1onCourt.values():
                    print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
                print(t2 + " Subs:")
                for p in gs.t2onCourt.values():
                    print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
                gs.currShotClock = gs.shotClock
                gs.currTime = gs.qtrTime
                gs.crossed_midcourt = False
                if gs.possTeam == t1:
                    gs.possPlayer = random.choice(list(gs.t1onCourt.values()))
                    print(
                        gs.possPlayer["position"]
                        + " "
                        + gs.possPlayer["first_name"]
                        + " "
                        + gs.possPlayer["last_name"]
                        + " takes the ball out to begin the "
                        + ("half " if gs.league == "CBB" else "quarter ")
                        + "for "
                        + gs.possTeam
                        + "."
                    )
                    gs.finalHeavePending = True
                    gs.courtPos = (4, 3)
                elif gs.possTeam == t2:
                    gs.possPlayer = random.choice(list(gs.t2onCourt.values()))
                    print(
                        gs.possPlayer["position"]
                        + " "
                        + gs.possPlayer["first_name"]
                        + " "
                        + gs.possPlayer["last_name"]
                        + " takes the ball out to begin the "
                        + ("half " if gs.league == "CBB" else "quarter ")
                        + "for "
                        + gs.possTeam
                        + "."
                    )
                    gs.finalHeavePending = True
                    gs.courtPos = (-4, 3)
                gs.periodOn = True
            elif gs.period >= gs.periodPerGame and gs.t1pts == gs.t2pts:
                print("We're headed to overtime!")
                gs.period += 1
                gs.lastCountedPossessionTeam = None
                otAdd = 1 if gs.league == "CBB" else 2
                gs.teamTimeoutsRemaining[t1] += otAdd
                gs.teamTimeoutsRemaining[t2] += otAdd
                print(
                    f"Overtime timeout allocation: {t1} and {t2} each receive {otAdd} additional timeout{'s' if otAdd != 1 else ''}."
                )
                gs.applyFatigueRecovery(overtimeBreakRecoveryMinutes, "Overtime breather")
                gs.dampenMomentum(momentumOvertimeBreakRetention, "overtime break")
                gs.currShotClock = gs.shotClock
                gs.currTime = gs.otQtrTime
                gs.t1onCourt, gs.t2onCourt, gs.lineupParameters = gs.pullSubs(True)
                print(t1 + " Subs:")
                for p in gs.t1onCourt.values():
                    print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
                print(t2 + " Subs:")
                for p in gs.t2onCourt.values():
                    print(p['position'] + " " + p['first_name'] + " " + p['last_name'])
                gs.crossed_midcourt = False
                gs.courtPos = (0, 3)
                gs.possTeam = "OT_TIPOFF"
                gs.periodOn = True
            else:
                print("End of the game.")
                gs.gameOn = False

    # ------------------------------------------------------------------ final stats
    gs.t1stats["MP"] = (gs.t1stats["MP"] / 60).round(2)
    gs.t1stats['Pts'] = (
        (gs.t1stats['FT Shot Made'] * 1)
        + (gs.t1stats['Ins Shot Made'] * 2)
        + (gs.t1stats['Mid Shot Made'] * 2)
        + (gs.t1stats['3PT Shot Made'] * 3)
    )
    gs.t1stats['TREB'] = gs.t1stats['DREB'] + gs.t1stats['OREB']
    gs.t2stats["MP"] = (gs.t2stats["MP"] / 60).round(2)
    gs.t2stats['Pts'] = (
        (gs.t2stats['FT Shot Made'] * 1)
        + (gs.t2stats['Ins Shot Made'] * 2)
        + (gs.t2stats['Mid Shot Made'] * 2)
        + (gs.t2stats['3PT Shot Made'] * 3)
    )
    gs.t2stats['TREB'] = gs.t2stats['DREB'] + gs.t2stats['OREB']
    for stats in (gs.t1stats, gs.t2stats):
        for col, att, made in [
            ('Ins Shot %', 'Ins Shot Att', 'Ins Shot Made'),
            ('Mid Shot %', 'Mid Shot Att', 'Mid Shot Made'),
            ('3PT Shot %', '3PT Shot Att', '3PT Shot Made'),
            ('FT Shot %', 'FT Shot Att', 'FT Shot Made'),
        ]:
            try:
                stats[col] = (stats[made] / stats[att]).round(4) * 100
            except ZeroDivisionError:
                stats[col] = 0
    for ts, stats in [(gs.t1teamstats, gs.t1stats), (gs.t2teamstats, gs.t2stats)]:
        for col, att, made in [
            ('Ins Shot %', 'Ins Shot Att', 'Ins Shot Made'),
            ('Mid Shot %', 'Mid Shot Att', 'Mid Shot Made'),
            ('3PT Shot %', '3PT Shot Att', '3PT Shot Made'),
            ('FT Shot %', 'FT Shot Att', 'FT Shot Made'),
        ]:
            try:
                ts[col] = (stats[made].sum() / stats[att].sum()).round(4) * 100
            except ZeroDivisionError:
                ts[col] = 0
        ts['Ins Shot Att'] = stats['Ins Shot Att'].sum()
        ts['Ins Shot Made'] = stats['Ins Shot Made'].sum()
        ts['Mid Shot Att'] = stats['Mid Shot Att'].sum()
        ts['Mid Shot Made'] = stats['Mid Shot Made'].sum()
        ts['3PT Shot Att'] = stats['3PT Shot Att'].sum()
        ts['3PT Shot Made'] = stats['3PT Shot Made'].sum()
        ts['FT Shot Att'] = stats['FT Shot Att'].sum()
        ts['FT Shot Made'] = stats['FT Shot Made'].sum()
        ts['TREB'] = stats['DREB'].sum() + stats['OREB'].sum()
        ts['OREB'] = stats['OREB'].sum()
        ts['DREB'] = stats['DREB'].sum()
        ts['Stl'] = stats['Stl'].sum()
        ts['Blk'] = stats['Blk'].sum()
        ts['TO'] = stats['TO'].sum()
        ts['Foul'] = stats['Foul'].sum()
        ts['Assist'] = stats['Assist'].sum()
    gs.t1teamstats['Poss'] = gs.teamPossessions[t1]
    gs.t1teamstats['TOP'] = f"{int(gs.teamPossessionTime[t1] // 60):02d}:{gs.teamPossessionTime[t1] % 60:04.1f}"
    gs.t1teamstats['Pts'] = (
        (gs.t1stats['FT Shot Made'].sum() * 1)
        + (gs.t1stats['Ins Shot Made'].sum() * 2)
        + (gs.t1stats['Mid Shot Made'].sum() * 2)
        + (gs.t1stats['3PT Shot Made'].sum() * 3)
    )
    gs.t2teamstats['Poss'] = gs.teamPossessions[t2]
    gs.t2teamstats['TOP'] = f"{int(gs.teamPossessionTime[t2] // 60):02d}:{gs.teamPossessionTime[t2] % 60:04.1f}"
    gs.t2teamstats['Pts'] = (
        (gs.t2stats['FT Shot Made'].sum() * 1)
        + (gs.t2stats['Ins Shot Made'].sum() * 2)
        + (gs.t2stats['Mid Shot Made'].sum() * 2)
        + (gs.t2stats['3PT Shot Made'].sum() * 3)
    )
    gs.t1teamscore['P1'] = gs.t1q1pts
    gs.t1teamscore['P2'] = gs.t1q2pts
    gs.t1teamscore['P3'] = gs.t1q3pts
    gs.t1teamscore['P4'] = gs.t1q4pts
    gs.t1teamscore['OT'] = gs.t1qotpts
    gs.t1teamscore['F'] = gs.t1q1pts + gs.t1q2pts + gs.t1q3pts + gs.t1q4pts + gs.t1qotpts
    gs.t2teamscore['P1'] = gs.t2q1pts
    gs.t2teamscore['P2'] = gs.t2q2pts
    gs.t2teamscore['P3'] = gs.t2q3pts
    gs.t2teamscore['P4'] = gs.t2q4pts
    gs.t2teamscore['OT'] = gs.t2qotpts
    gs.t2teamscore['F'] = gs.t2q1pts + gs.t2q2pts + gs.t2q3pts + gs.t2q4pts + gs.t2qotpts
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    teamscore = pd.concat([gs.t1teamscore, gs.t2teamscore], axis=0)
    teamstats = pd.concat([gs.t1teamstats, gs.t2teamstats], axis=0)
    print(teamscore)
    print(teamstats)
    print(gs.t1stats[gs.t1stats["MP"] > 0.00])
    print(gs.t2stats[gs.t2stats["MP"] > 0.00])
    return teamscore, teamstats, gs.t1stats, gs.t2stats

    # results = MatchResults(
    #     team_one, team_two, t1State.Roster, t2State.Roster, gameid, is_nba
    # )

    # return results
