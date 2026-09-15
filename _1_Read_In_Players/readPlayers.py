from datetime import date
from _DClasses.flashscoreDataClasses import FlashscoreData
from _DClasses.proballersDataClasses import ProballersData
from _DClasses.report import Report
from _DClasses.player import Player, PlayerData
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

playerLinksFile = Path(
    os.getenv("PLAYER_LINKS_FILE", "_Data/playerLinks.csv")
) 

def readPlayers():
    
    report = Report()

    db = pd.read_csv(playerLinksFile)

    for row in db.itertuples(index=False):
        name, lastPlayed, proballersData, flashscoreData = row
        [proballersID, proballersName] = proballersData.split("|")
        [flashscoreName, flashscoreID] = flashscoreData.split("|")
        playerData = PlayerData(
            proballers = ProballersData(
                id=proballersID,
                name=proballersName
            ),
            flashscore = FlashscoreData(
                id=flashscoreID,
                name=flashscoreName
            )
        )
        report.players.append(
            Player(
                name=name,
                last_game=date.fromisoformat(lastPlayed),
                playerData=playerData
            )
        )

    return report