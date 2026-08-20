```
// The large response object returning
type MatchStateResponse struct {
	MatchType string
	Week      uint
	Matches   []MatchResponse
}

// An individual match object for the engine
type MatchResponse struct {
	ID                     uint
	MatchName              string // For Post-Season matchups
	WeekID                 uint
	Week                   uint
	SeasonID               uint
	HomeTeamID             uint
	HomeTeam               string
	AwayTeamID             uint
	AwayTeam               string
	MatchOfWeek            string
	Arena                  string
	Capacity               int
	City                   string
	State                  string
	IsNeutralSite          bool
	IsNBAMatch             bool
	IsConference           bool
	IsConferenceTournament bool
	IsNITGame              bool
	IsPlayoffGame          bool
	IsNationalChampionship bool
	IsRivalryGame          bool
	IsInvitational         bool
	IsInternational        bool
	Channel                uint
	MatchData              MatchDataResponse
}

// The game data needed to run a match
type MatchDataResponse struct {
	HomeTeam           MatchTeamResponse
	HomeTeamRoster     []GamePlayer
	HomeTeamGameplan   Gameplan
	HomeTeamLineup     []GameplanLineup
	AwayTeam           MatchTeamResponse
	AwayTeamRoster     []GamePlayer
	AwayTeamGameplan   Gameplan
	AwayTeamLineup     []GameplanLineup
	League             string
	HomeCourtAdvantage float64
}

type MatchTeamResponse struct {
	ID           uint
	TeamName     string
	Mascot       string
	Abbr         string
	Conference   string
	Coach        string
	ConferenceID uint
	LeagueID     uint
}

type Gameplan struct {
	gorm.Model
	TeamID               uint
	Game                 string
	Pace                 string
	ThreePointProportion int
	JumperProportion     int
	PaintProportion      int
	FocusPlayer          string
	OffensiveFormation   string
	DefensiveFormation   string
	OffensiveStyle       string
	Toggle2pt            bool
	Toggle3pt            bool
	ToggleFT             bool
	ToggleFN             bool
	ToggleBW             bool
	ToggleRB             bool
	ToggleID             bool
	TogglePD             bool
	ToggleP2             bool
	ToggleP3             bool
	PreserveTimeouts     bool
	Trigger1Enabled      bool
	Trigger1Type         uint8 // 1 == Designated Player, 2 == Fouls Per Half
	Trigger1Value        uint  // Could either be player ID or number of fouls per half
	Trigger2Enabled      bool
	Trigger2Value        uint // Number of points the opponent is up by
	Trigger3Enabled      bool // Designate Player Exhaustion Trigger
	Trigger3Value        uint // PlayerID of the player to monitor for exhaustion
	Trigger3Exhaustion   uint // Exhaustion threshold for the designated player
	Trigger4Enabled      bool // On-floor average exhaustion
	Trigger4Value        uint // Average exhaustion of all players on the floor
}


type GameplanLineup struct {
	gorm.Model         // Just ignore this, it's for GORM (primary ID).
	TeamID             uint
	Position           string // G, F, or C
	FirstStringID      uint   // PlayerID at first string
	FSMinutes          uint8
	FSInsideProportion uint8 // Proportion towards shooting inside shots
	FSMidProportion    uint8 // Proportion towards shooting midrange shots
	FSThreeProportion  uint8 // Proportion towards shooting three point shots
	SecondStringID     uint  // PlayerID at second string
	SSMinutes          uint8
	SSInsideProportion uint8
	SSMidProportion    uint8
	SSThreeProportion  uint8
	ThirdStringID      uint // PlayerID at third string
	TSMinutes          uint8
	TSInsideProportion uint8
	TSMidProportion    uint8
	TSThreeProportion  uint8
}

type GamePlayer struct {
	ID uint
	BasePlayer
	// Dont worry about the Mod properties
	InsideShootingMod     float64
	MidRangeShootingMod   float64
	ThreePointShootingMod float64
	FreeThrowMod          float64
	AgilityMod            float64
	BallworkingMod        float64
	StealingMod           float64
	BlockingMod           float64
	ReboundingMod         float64
	InteriorDefenseMod    float64
	PerimeterDefenseMod   float64
}

type BasePlayer struct {
	TeamID                 uint
	Team                   string
	PlayerID               uint
	FirstName              string
	LastName               string
	Position               string
	Archetype              string
	Age                    uint8
	PrimeAge               uint8
	Year                   uint8
	City                   string
	HighSchool             string
	State                  string
	Country                string
	Stars                  uint8
	Height                 uint8
	Weight                 uint16
	BasketballIQ           uint8
	SpecBasketballIQ       bool
	InsideShooting         uint8
	SpecInsideShooting     bool
	MidRangeShooting       uint8
	SpecMidRangeShooting   bool
	ThreePointShooting     uint8
	SpecThreePointShooting bool
	FreeThrow              uint8
	SpecFreeThrow          bool
	Agility                uint8
	SpecAgility            bool
	Ballwork               uint8
	SpecBallwork           bool
	Rebounding             uint8
	SpecRebounding         bool
	Stealing               uint8
	SpecStealing           bool
	Blocking               uint8
	SpecBlocking           bool
	InteriorDefense        uint8
	SpecInteriorDefense    bool
	PerimeterDefense       uint8
	SpecPerimeterDefense   bool
	Potential              uint8
	PotentialGrade         string
	ProPotentialGrade      uint8
	Stamina                uint8
	Discipline             uint8
	InjuryRating           uint8
	IsInjured              bool
	InjuryName             string
	InjuryType             string
	WeeksOfRecovery        uint8
	InjuryReserve          bool
	PlaytimeExpectations   uint8
	Overall                uint8
	SpecCount              uint8
	Personality            string
	FreeAgency             string
	RecruitingBias         string
	RecruitingBiasValue    string
	WorkEthic              string
	AcademicBias           string
	PreviousTeamID         uint
	PreviousTeam           string
	RelativeID             uint8
	RelativeType           uint8
	Notes                  string
	IsInjuryReserve        bool
	PlayerPreferences
}
```
