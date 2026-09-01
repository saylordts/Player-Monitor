from datetime import date
from _DClasses.report import Report
from _DClasses.player import Player
import pandas as pd

def readPlayers():
    
    report = Report()

    db = pd.read_csv("_Data/playerLinks.csv")

    for row in db.itertuples(index=False):
        name, lastPlayed, proballersLink, flashscoreLink = row
        report.players.append(
            Player(
                name=name,
                last_game=date.fromisoformat(lastPlayed),
                links={"proballers": proballersLink, "flashscore": flashscoreLink}
            )
        )

    return report