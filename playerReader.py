from datetime import date
from DClasses.report import Report
from DClasses.player import Player
import pandas as pd

def readPlayers():
    with open("Data/playerList.txt", "r") as file:
        playerList = file.read().splitlines()

    report = Report()

    df = pd.read_csv("Data/players.csv") 

    for playerURL in playerList:
        matching_row = df[df["URL"] == playerURL]
        if not matching_row.empty:
            last_game_unformatted = matching_row["Last Played"].values[0]
        else:
            last_game_unformatted = "1900-01-01"
            
        last_game = date.fromisoformat(last_game_unformatted)
        
        last_game_unformatted = "1900-01-01"    # TAKE ME OUT
        last_game = date.fromisoformat(last_game_unformatted) # TAKE ME OUT
        report.players.append(
            Player(
                URL = playerURL,
                last_game = last_game
                )
            )
    return report