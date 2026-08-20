injuryProbability = 0.0001

#Close to Goal Probabilities
stealProbability = 0.002
otherTurnoverProbability = 0.0015
moveAttemptProbability = 0.3935
passAttemptProbability = 0.383
shotAttemptProbability = 0.22

# Offensive destination tendencies. These are neutral baseline values and can later be modified by each team's gameplan.
threePointDestinationWeight = 0.75
midrangeDestinationWeight = 1.00
insideDestinationWeight = 6.00

#TO Cutoffs
outOfBounds = 0.784
foulBall = 1

#Shot Baselines
ftMagicNum1 = 0.008
ftMagicNum2 = 0.55

cbb_ins_base = 0.4325
cbb_ins_adj = 0.015
cbb_mid_base = 0.4125
cbb_mid_adj = 0.0125
cbb_three_base = 0.3
cbb_three_adj = 0.0125

nba_ins_base = 0.383
nba_ins_adj = 0.007
nba_mid_base = 0.305
nba_mid_adj = 0.007
nba_three_base = 0.23
nba_three_adj = 0.007

# Pass Pressure
passPressureAdjustmentPerPoint = 0.005
passMaximumEffectiveGap = 15.0
passDeflectionMinimum = 0.01
passDeflectionMaximum = 0.40

# Shot Defense
shotAverageDefenseRating = 20.0
shotDefenseAdjustmentPerPoint = 0.004
shotDefenseMaximumAdjustment = 0.06

# Blocks
blockInsideBaseline = 0.120
blockPaintBaseline = 0.090
blockMidrangeBaseline = 0.0375
blockThreeBaseline = 0.015
blockCornerThreeBaseline = 0.015

blockAverageRating = 20.0
blockRatingAdjustmentPerPoint = 0.003
blockMaximumRatingAdjustment = 0.03

blockHeightAdjustmentPerInch = 0.001
blockMaximumHeightAdjustment = 0.01

blockChanceMinimum = 0.001
blockChanceMaximum = 0.15

# Dunk Narration
insideDunkThreshold = 0.35
paintDriveDunkThreshold = 0.35
paintPosterDunkThreshold = 0.10

# Shooting Fouls
shootingFoulInsideBaseline = 0.15000
shootingFoulPaintBaseline = 0.11250
shootingFoulMidrangeBaseline = 0.03750
shootingFoulThreeBaseline = 0.01875
shootingFoulCornerThreeBaseline = 0.01688

shootingFoulAverageBBIQ = 20.0
shootingFoulBBIQModifierPerPoint = 0.02
shootingFoulMaximumBBIQGap = 15.0

shootingFoulChanceMinimum = 0.001
shootingFoulChanceMaximum = 0.18
shootingFoulMadeShotModifier = 0.55

# Non-Shooting Fouls
nonShootingFoulInsideBaseline = 0.034000
nonShootingFoulPaintBaseline = 0.028000
nonShootingFoulMidrangeBaseline = 0.020000
nonShootingFoulPerimeterBaseline = 0.014000
nonShootingFoulBackcourtBaseline = 0.009000

nonShootingFoulChanceMinimum = 0.001
nonShootingFoulChanceMaximum = 0.08

# Offensive Fouls
offensiveFoulInsideBaseline = 0.025
offensiveFoulPaintBaseline = 0.015
offensiveFoulMidrangeBaseline = 0.005
offensiveFoulPerimeterBaseline = 0.002
offensiveFoulBackcourtBaseline = 0.001

offensiveFoulAverageBBIQ = 20.0
offensiveFoulOffensiveBBIQModifierPerPoint = 0.02
offensiveFoulDefenderBBIQModifierPerPoint = 0.01
offensiveFoulMaximumBBIQGap = 15.0

offensiveFoulChanceMinimum = 0.0005
offensiveFoulChanceMaximum = 0.05

# Stamina
staminaNormalMaximumPenalty = 0.30
staminaExcessPenaltyPerRatio = 0.20
staminaMinimumModifier = 0.50

halftimeRecoveryMinutes = 3.0
quarterBreakRecoveryMinutes = 1.5
overtimeBreakRecoveryMinutes = 1.0
mediaTimeoutRecoveryMinutes = 0.75
teamTimeoutRecoveryMinutes = 0.50

# Shot-clock urgency
shotClockUrgencyStart = 10.0
shotClockUrgencyMaximumBonus = 0.35
shotClockUrgencyMaximumShotProbability = 0.85
shotClockAwarenessAverageBBIQ = 20.0
shotClockAwarenessMaximumBBIQGap = 10.0
shotClockAwarenessModifierPerPoint = 0.025

# Final heaves
finalHeaveMaximumTime = 3.0
finalHeaveDifficultyMultiplier = 0.15
finalHeaveMinimumChance = 0.01
finalHeaveMaximumChance = 0.10

# Momentum
momentumMadeTwoSwing = 0.08
momentumMadeThreeSwing = 0.12
momentumDunkSwing = 0.12
momentumPosterDunkSwing = 0.16
momentumMissSwing = 0.04
momentumStealSwing = 0.10
momentumBlockSwing = 0.10

momentumMediaTimeoutRetention = 0.75
momentumTeamTimeoutRetention = 0.75
momentumHalftimeRetention = 0.10
momentumQuarterBreakRetention = 0.60
momentumOvertimeBreakRetention = 0.75

momentumMaximumAttributeBonus = 0.05
