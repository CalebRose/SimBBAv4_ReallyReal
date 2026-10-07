import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

from endpoints import GetMatchesForSimulation, SendResults
from game_log import render_game_log
from simulation import rungame
from import_dto import ImportDTO, MatchResults, Team


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


matchState = GetMatchesForSimulation()
if not matchState:
    print("Failed to fetch matches from the API.")
    sys.exit(1)

is_testing = False
logDirectory = Path(__file__).resolve().parent / "game_logs"
if is_testing:
    logDirectory.mkdir(exist_ok=True)
cbb_result_list = []
nba_result_list = []
matches = matchState.get("Matches", [])
if not matches:
    print("No matches returned from the API.")
    sys.exit(0)

for gameNumber, match in enumerate(matches, start=1):
    matchData = match.get("MatchData", {})
    gameId = match.get("ID", gameNumber)
    homeTeam = matchData.get("HomeTeam", {}).get("Abbr", "HOME")
    awayTeam = matchData.get("AwayTeam", {}).get("Abbr", "AWAY")

    with open(os.devnull, "w", encoding="utf-8") as quietOutput:
        with redirect_stdout(quietOutput):
            gs = rungame(match, gameNumber)

    if is_testing:
        logPath = logDirectory / f"game_{gameId}_{homeTeam}_vs_{awayTeam}.txt"
        with logPath.open("w", encoding="utf-8", buffering=1) as logFile:
            with redirect_stdout(TeeOutput(sys.stdout, logFile)):
                for line in render_game_log(gs):
                    print(line)
                print(f"Complete game output written to: {logPath}")

    home = matchData["HomeTeam"]
    away = matchData["AwayTeam"]
    t1 = Team(home)
    t1.Stats = gs.t1TeamStatsDTO
    t2 = Team(away)
    t2.Stats = gs.t2TeamStatsDTO
    results = MatchResults(
        t1,
        t2,
        gs.playerStatsDTOs,
        gameId,
        matchData.get("League", "") == "NBA",
        gs.pbp.to_list()
    )
    if matchData.get("League", "") == "NBA":
        nba_result_list.append(results)
    else:
        cbb_result_list.append(results)
dto = ImportDTO(cbb_result_list, nba_result_list)
SendResults(dto) 