import sys
from contextlib import redirect_stdout
from pathlib import Path

from endpoints import GetMatchesForSimulation
from simulation import rungame


class TeeOutput:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, text):
        for output in self.outputs:
            output.write(text)
        return len(text)

    def flush(self):
        for output in self.outputs:
            output.flush()


logDirectory = Path(__file__).resolve().parent / "game_logs"
logDirectory.mkdir(exist_ok=True)


matchState = GetMatchesForSimulation()
if not matchState:
    print("Failed to fetch matches from the API.")
    sys.exit(1)

matches = matchState.get("Matches", [])
if not matches:
    print("No matches returned from the API.")
    sys.exit(0)

for gameNumber, match in enumerate(matches, start=1):
    matchData = match.get("MatchData", {})
    gameId = match.get("ID", gameNumber)
    homeTeam = matchData.get("HomeTeam", {}).get("Abbr", "HOME")
    awayTeam = matchData.get("AwayTeam", {}).get("Abbr", "AWAY")

    logPath = logDirectory / f"game_{gameId}_{homeTeam}_vs_{awayTeam}.txt"
    with logPath.open("w", encoding="utf-8", buffering=1) as logFile:
        with redirect_stdout(TeeOutput(sys.stdout, logFile)):
            rungame(match, gameNumber)
            print(f"Complete game output written to: {logPath}")

# dto = ImportDTO(cbb_result_list, nba_result_list)
# SendStats(dto)