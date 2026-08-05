import sys
from contextlib import redirect_stdout
from pathlib import Path

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


gameId = 1
homeTeam = "SCHS"
awayTeam = "TCHS"
league = "CBB"
homeCourtAdvantage = 0
gameNumber = 1

logDirectory = Path(__file__).resolve().parent / "game_logs"
logDirectory.mkdir(exist_ok=True)
logPath = logDirectory / f"game_{gameId}_{homeTeam}_vs_{awayTeam}.txt"

with logPath.open("w", encoding="utf-8", buffering=1) as logFile:
    with redirect_stdout(TeeOutput(sys.stdout, logFile)):
        rungame(gameId, homeTeam, awayTeam, league, homeCourtAdvantage, gameNumber)
        print(f"Complete game output written to: {logPath}")
