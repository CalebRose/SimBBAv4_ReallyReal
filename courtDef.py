import random
from baseprobabilities import *

COURT_X_MIN = -4
COURT_X_MAX = 4
COURT_Y_MIN = 1
COURT_Y_MAX = 5

INSIDE_SPOTS = {
    (-4, 3), (4, 3)
}

PAINT_SPOTS = {
    (-3, 3), (3, 3)
}

MID_RANGE_SPOTS = {
    (-4, 2), (-3, 2), (-2, 2), (-2, 3),
    (-4, 4), (-3, 4), (-2, 4),
    (4, 2), (3, 2), (2, 2), (2, 3),
    (4, 4), (3, 4), (2, 4)
}

THREE_POINT_SPOTS = {
    (-3, 1), (-2, 1), (-1, 1),
    (-1, 2), (-1, 3), (-1, 4), (-1, 5),
    (-2, 5), (-3, 5),
    (3, 1), (2, 1), (1, 1),
    (1, 2), (1, 3), (1, 4), (1, 5),
    (2, 5), (3, 5)
}

CORNER_THREE_SPOTS = {
    (-4, 1), (-4, 5),
    (4, 1), (4, 5)
}

SHOT_CHANCES = {
    "inside": 0.40,
    "paint": 0.28,
    "midrange": 0.18,
    "three": 0.22,
    "corner_three": 0.25
}

NON_SHOT_ACTIONS = {
    "move": 0.45,
    "pass": 0.45,
    "turnover": 0.10
}

PASS_TURNOVER_BY_DISTANCE = {
    1: 0.017,
    2: 0.034,
    3: 0.060,
    4: 0.085,
    5: 0.120,
    6: 0.155,
    7: 0.190,
    8: 0.230
}

def is_valid_spot(courtPos):
    x, y = courtPos
    return COURT_X_MIN <= x <= COURT_X_MAX and COURT_Y_MIN <= y <= COURT_Y_MAX

def get_shot_zone(courtPos):
    if courtPos in INSIDE_SPOTS:
        return "inside"
    elif courtPos in PAINT_SPOTS:
        return "paint"
    elif courtPos in MID_RANGE_SPOTS:
        return "midrange"
    elif courtPos in THREE_POINT_SPOTS:
        return "three"
    elif courtPos in CORNER_THREE_SPOTS:
        return "corner_three"
    return None

def get_movement_defense(defender,position,staminaModifier=1.0):
    zone = get_shot_zone(position)

    perimeter_defense = float(defender["perimeter_defense"]) * staminaModifier
    interior_defense = float(defender["interior_defense"]) * staminaModifier

    if zone in ("three", "corner_three"):
        return perimeter_defense, "perimeter"

    if zone == "midrange":
        movement_defense = (
            perimeter_defense + interior_defense
        ) / 2

        return movement_defense, "blend"

    if zone in ("inside", "paint"):
        return interior_defense, "interior"

    # Backcourt or midcourt positions are not shooting zones,
    # but movement is still defended primarily on the perimeter.
    if zone is None:
        return perimeter_defense, "perimeter"

    raise ValueError(
        f"Unsupported movement-defense zone: {zone} "
        f"for position {position}"
    )

def get_shot_defense_adjustment(defender,courtPos,staminaModifier=1.0):
    shotDefense,shotDefenseType = get_movement_defense(defender,courtPos,staminaModifier)

    defenseDifference = shotAverageDefenseRating - shotDefense
    shotDefenseAdjustment = defenseDifference * shotDefenseAdjustmentPerPoint
    shotDefenseAdjustment = max(-shotDefenseMaximumAdjustment,min(shotDefenseMaximumAdjustment,shotDefenseAdjustment))

    return shotDefenseAdjustment,shotDefense,shotDefenseType

def get_shooting_foul_chance(defender, courtPos):
    zone = get_shot_zone(courtPos)

    foulBaselineByZone = {
        "inside": shootingFoulInsideBaseline,
        "paint": shootingFoulPaintBaseline,
        "midrange": shootingFoulMidrangeBaseline,
        "three": shootingFoulThreeBaseline,
        "corner_three": shootingFoulCornerThreeBaseline,
    }

    if zone not in foulBaselineByZone:
        raise ValueError(f"Unsupported shooting-foul zone: {zone} for position {courtPos}")

    zoneFoulBaseline = foulBaselineByZone[zone]
    foulDefenderIQ = float(defender["bbiq"])
    bbiqDifference = shootingFoulAverageBBIQ - foulDefenderIQ
    effectiveBBIQDifference = max(-shootingFoulMaximumBBIQGap, min(shootingFoulMaximumBBIQGap, bbiqDifference))
    bbiqFoulModifier = 1.0 + (effectiveBBIQDifference * shootingFoulBBIQModifierPerPoint)
    shootingFoulChance = zoneFoulBaseline * bbiqFoulModifier
    shootingFoulChance = max(shootingFoulChanceMinimum, min(shootingFoulChanceMaximum, shootingFoulChance))

    return shootingFoulChance, zoneFoulBaseline, foulDefenderIQ, bbiqFoulModifier

def get_non_shooting_foul_chance(defender,targetPos):
    zone = get_shot_zone(targetPos)

    foulBaselineByZone = {
        "inside": nonShootingFoulInsideBaseline,
        "paint": nonShootingFoulPaintBaseline,
        "midrange": nonShootingFoulMidrangeBaseline,
        "three": nonShootingFoulPerimeterBaseline,
        "corner_three": nonShootingFoulPerimeterBaseline,
        None: nonShootingFoulBackcourtBaseline,
    }

    if zone not in foulBaselineByZone:
        raise ValueError(f"Unsupported non-shooting-foul zone: {zone} for position {targetPos}")

    zoneFoulBaseline = foulBaselineByZone[zone]
    foulDefenderIQ = float(defender["bbiq"])
    bbiqDifference = shootingFoulAverageBBIQ - foulDefenderIQ
    effectiveBBIQDifference = max(-shootingFoulMaximumBBIQGap,min(shootingFoulMaximumBBIQGap,bbiqDifference))
    bbiqFoulModifier = 1.0 + (effectiveBBIQDifference * shootingFoulBBIQModifierPerPoint)
    nonShootingFoulChance = zoneFoulBaseline * bbiqFoulModifier
    nonShootingFoulChance = max(nonShootingFoulChanceMinimum,min(nonShootingFoulChanceMaximum,nonShootingFoulChance))

    return nonShootingFoulChance,zoneFoulBaseline,foulDefenderIQ,bbiqFoulModifier

def get_offensive_foul_chance(offensivePlayer,defender,targetPos):
    zone = get_shot_zone(targetPos)

    foulBaselineByZone = {
        "inside": offensiveFoulInsideBaseline,
        "paint": offensiveFoulPaintBaseline,
        "midrange": offensiveFoulMidrangeBaseline,
        "three": offensiveFoulPerimeterBaseline,
        "corner_three": offensiveFoulPerimeterBaseline,
        None: offensiveFoulBackcourtBaseline,
    }

    if zone not in foulBaselineByZone:
        raise ValueError(f"Unsupported offensive-foul zone: {zone} for position {targetPos}")

    zoneFoulBaseline = foulBaselineByZone[zone]
    offensivePlayerIQ = float(offensivePlayer["bbiq"])
    foulDefenderIQ = float(defender["bbiq"])

    offensiveBBIQDifference = offensiveFoulAverageBBIQ - offensivePlayerIQ
    effectiveOffensiveBBIQDifference = max(-offensiveFoulMaximumBBIQGap,min(offensiveFoulMaximumBBIQGap,offensiveBBIQDifference))
    offensiveBBIQModifier = 1.0 + (effectiveOffensiveBBIQDifference * offensiveFoulOffensiveBBIQModifierPerPoint)

    defenderBBIQDifference = foulDefenderIQ - offensiveFoulAverageBBIQ
    effectiveDefenderBBIQDifference = max(-offensiveFoulMaximumBBIQGap,min(offensiveFoulMaximumBBIQGap,defenderBBIQDifference))
    defenderBBIQModifier = 1.0 + (effectiveDefenderBBIQDifference * offensiveFoulDefenderBBIQModifierPerPoint)

    offensiveFoulChance = zoneFoulBaseline * offensiveBBIQModifier * defenderBBIQModifier
    offensiveFoulChance = max(offensiveFoulChanceMinimum,min(offensiveFoulChanceMaximum,offensiveFoulChance))

    return offensiveFoulChance,zoneFoulBaseline,offensivePlayerIQ,offensiveBBIQModifier,foulDefenderIQ,defenderBBIQModifier

def get_block_chance(defender,shootPlayer,courtPos,staminaModifier=1.0):
    zone = get_shot_zone(courtPos)

    blockBaselineByZone = {
        "inside": blockInsideBaseline,
        "paint": blockPaintBaseline,
        "midrange": blockMidrangeBaseline,
        "three": blockThreeBaseline,
        "corner_three": blockCornerThreeBaseline,
    }

    if zone not in blockBaselineByZone:
        raise ValueError(
            f"Unsupported block zone: {zone} "
            f"for position {courtPos}"
        )

    zoneBlockBaseline = (
        blockBaselineByZone[zone]
    )

    blockRating = float(defender["block"]) * staminaModifier

    blockRatingDifference = (
        blockRating - blockAverageRating
    )

    blockRatingAdjustment = (
        blockRatingDifference
        * blockRatingAdjustmentPerPoint
    )

    blockRatingAdjustment = max(
        -blockMaximumRatingAdjustment,
        min(
            blockMaximumRatingAdjustment,
            blockRatingAdjustment,
        ),
    )

    defenderHeight = float(
        defender["height"]
    )
    shooterHeight = float(
        shootPlayer["height"]
    )

    heightDifference = (
        defenderHeight - shooterHeight
    )

    heightAdjustment = (
        heightDifference
        * blockHeightAdjustmentPerInch
    )

    heightAdjustment = max(
        -blockMaximumHeightAdjustment,
        min(
            blockMaximumHeightAdjustment,
            heightAdjustment,
        ),
    )

    blockChance = (
        zoneBlockBaseline
        + blockRatingAdjustment
        + heightAdjustment
    )

    blockChance = max(
        blockChanceMinimum,
        min(
            blockChanceMaximum,
            blockChance,
        ),
    )

    return (
        blockChance,
        zoneBlockBaseline,
        blockRating,
        blockRatingAdjustment,
        defenderHeight,
        shooterHeight,
        heightAdjustment,
    )

def get_movement_success_probability(
    movementOffense,
    movementDefense
):
    ratingDifference = (
        float(movementOffense)
        - float(movementDefense)
    )

    minimumSuccess = 0.1
    defenderAdvantageSuccess = 0.50
    equalRatingSuccess = 0.60
    maximumSuccess = 0.9

    minimumDifference = -15.0
    defenderAdvantageDifference = -2.0
    maximumDifference = 15.0

    if ratingDifference <= minimumDifference:
        return minimumSuccess

    if ratingDifference < defenderAdvantageDifference:
        progress = (
            ratingDifference - minimumDifference
        ) / (
            defenderAdvantageDifference
            - minimumDifference
        )

        return (
            minimumSuccess
            + progress
            * (
                defenderAdvantageSuccess
                - minimumSuccess
            )
        )

    if ratingDifference < 0:
        progress = (
            ratingDifference
            - defenderAdvantageDifference
        ) / (
            0
            - defenderAdvantageDifference
        )

        return (
            defenderAdvantageSuccess
            + progress
            * (
                equalRatingSuccess
                - defenderAdvantageSuccess
            )
        )

    if ratingDifference < maximumDifference:
        progress = (
            ratingDifference
            / maximumDifference
        )

        return (
            equalRatingSuccess
            + progress
            * (
                maximumSuccess
                - equalRatingSuccess
            )
        )

    return maximumSuccess
def get_adjacent_spots(courtPos):
    x, y = courtPos
    spots = [
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y),     (x, y),     (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    ]
    return [spot for spot in spots if is_valid_spot(spot)]

def can_occupy_spot(team_side, newPos, crossed_midcourt):
    x, y = newPos

    if not is_valid_spot(newPos):
        return False

    if crossed_midcourt:
        if team_side == "HOME" and x < 0:
            return False
        if team_side == "AWAY" and x > 0:
            return False

    return True

def get_legal_move_spots(team_side, courtPos, crossed_midcourt):
    adjacent = get_adjacent_spots(courtPos)
    return [spot for spot in adjacent if can_occupy_spot(team_side, spot, crossed_midcourt)]

def get_legal_pass_targets(team_side, courtPos, crossed_midcourt):
    legal_spots = []
    for x in range(COURT_X_MIN, COURT_X_MAX + 1):
        for y in range(COURT_Y_MIN, COURT_Y_MAX + 1):
            spot = (x, y)
            if spot != courtPos and can_occupy_spot(team_side, spot, crossed_midcourt):
                legal_spots.append(spot)
    return legal_spots

def get_pass_distance(fromPos, toPos):
    x1, y1 = fromPos
    x2, y2 = toPos
    return max(abs(x2 - x1), abs(y2 - y1))

def get_pass_turnover_chance(fromPos, toPos):
    distance = get_pass_distance(fromPos, toPos)
    return PASS_TURNOVER_BY_DISTANCE.get(distance, 0.30)

def get_pass_deflection_chance(
    fromPos,
    toPos,
    passOffense,
    passDefense,
):
    distanceDeflectionChance = (
        get_pass_turnover_chance(
            fromPos,
            toPos,
        )
    )

    ratingDifference = (
        float(passDefense)
        - float(passOffense)
    )

    effectiveDifference = max(
        -passMaximumEffectiveGap,
        min(
            passMaximumEffectiveGap,
            ratingDifference,
        ),
    )

    passPressureAdjustment = (
        effectiveDifference
        * passPressureAdjustmentPerPoint
    )

    passDeflectionChance = (
        distanceDeflectionChance
        + passPressureAdjustment
    )

    return max(
        passDeflectionMinimum,
        min(
            passDeflectionMaximum,
            passDeflectionChance,
        ),
    )

def update_crossed_midcourt(team_side, courtPos, crossed_midcourt):
    x, y = courtPos

    if crossed_midcourt:
        return True

    if team_side == "HOME" and x >= 1:
        return True
    if team_side == "AWAY" and x <= -1:
        return True

    return False

def format_court_pos(courtPos):
    x, y = courtPos
    return f"({x},{y})"

def get_progress_value(team_side, fromPos, toPos):
    from_x, from_y = fromPos
    to_x, to_y = toPos

    if team_side == "HOME":
        return to_x - from_x
    elif team_side == "AWAY":
        return from_x - to_x

    return 0

def get_offensive_destination_weight(courtPos,destinationWeights=None):
    zone = get_shot_zone(courtPos)
    if zone in ("three","corner_three"):
        baseWeight = threePointDestinationWeight
        formationZone = "three"
    elif zone == "midrange":
        baseWeight = midrangeDestinationWeight
        formationZone = "midrange"
    elif zone in ("inside","paint"):
        baseWeight = insideDestinationWeight
        formationZone = "inside"
    else:
        baseWeight = 1.0
        formationZone = "neutral"
    if destinationWeights is None:
        return baseWeight
    return baseWeight * float(destinationWeights.get(formationZone,1.0))

def get_move_weight(team_side, fromPos, toPos, crossed_midcourt,destinationWeights=None):
    progress = get_progress_value(team_side, fromPos, toPos)

    # After midcourt, movement can be more natural/random
    if crossed_midcourt:
        if progress > 0:
            return 3 * get_offensive_destination_weight(toPos,destinationWeights)
        elif progress == 0:
            return 2 * get_offensive_destination_weight(toPos,destinationWeights)
        else:
            return 1 * get_offensive_destination_weight(toPos,destinationWeights)

    # Before midcourt, always push the ball forward
    if progress > 0:
        return 12
    elif progress == 0:
        return 3
    else:
        return 0.15

def get_pass_weight(team_side, fromPos, toPos, crossed_midcourt,destinationWeights=None):
    from_x, from_y = fromPos
    to_x, to_y = toPos

    progress = get_progress_value(team_side, fromPos, toPos)
    dx = abs(to_x - from_x)
    dy = abs(to_y - from_y)
    distance = get_pass_distance(fromPos, toPos)

    # Strong preference for short passes
    if distance == 1:
        distance_weight = 20
    elif distance == 2:
        distance_weight = 8
    elif distance == 3:
        distance_weight = 3
    elif distance == 4:
        distance_weight = 1.2
    elif distance == 5:
        distance_weight = 0.45
    elif distance == 6:
        distance_weight = 0.15
    else:
        distance_weight = 0.05

    # Penalize passes that move a lot vertically across the court
    # This makes cross-court zips much rarer
    if dy == 0:
        lateral_weight = 1.0
    elif dy == 1:
        lateral_weight = 0.9
    elif dy == 2:
        lateral_weight = 0.55
    elif dy == 3:
        lateral_weight = 0.25
    else:
        lateral_weight = 0.10

    # Before midcourt, strongly favor advancing the ball
    if crossed_midcourt is False:
        if progress > 0:
            progress_weight = 2.5
        elif progress == 0:
            progress_weight = 1.0
        else:
            progress_weight = 0.05
    else:
        # After midcourt, still prefer forward or neutral passes,
        # but much less aggressively
        if progress > 0:
            progress_weight = 1.25
        elif progress == 0:
            progress_weight = 1.0
        else:
            progress_weight = 0.6

    return distance_weight * lateral_weight * progress_weight * get_offensive_destination_weight(toPos,destinationWeights)

    # Before midcourt, strongly bias advancing passes
    if progress > 0:
        return distance_weight * 6
    elif progress == 0:
        return distance_weight * 1.5
    else:
        return distance_weight * 0.1

def choose_weighted_move_spot(team_side, courtPos, crossed_midcourt,destinationWeights=None):
    legal_spots = get_legal_move_spots(team_side, courtPos, crossed_midcourt)

    if len(legal_spots) == 0:
        return None

    weights = [
        get_move_weight(team_side, courtPos, spot, crossed_midcourt,destinationWeights)
        for spot in legal_spots
    ]

    return random.choices(legal_spots, weights=weights, k=1)[0]

def choose_weighted_pass_target(team_side, courtPos, crossed_midcourt,destinationWeights=None):
    legal_targets = get_legal_pass_targets(team_side, courtPos, crossed_midcourt)

    if len(legal_targets) == 0:
        return None

    weights = [
        get_pass_weight(team_side, courtPos, target, crossed_midcourt,destinationWeights)
        for target in legal_targets
    ]

    return random.choices(legal_targets, weights=weights, k=1)[0]

def is_in_frontcourt(team_side, courtPos):
    x, y = courtPos

    if team_side == "HOME":
        return x >= 1
    elif team_side == "AWAY":
        return x <= -1

    return False
