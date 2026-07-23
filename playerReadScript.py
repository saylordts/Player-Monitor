from report import Report
from player import Player
import csv
import pandas as pd

def readPlayers():
    with open("playerList.txt", "r") as file:
        playerList = file.read().splitlines()

    report = Report()

    df = pd.read_csv("players.csv") 

    for playerURL in playerList:
        matching_row = df[df["URL"] == playerURL]
        if not matching_row.empty:
            last_game = matching_row["Last Played"].values[0]
        else:
            last_game = "1900-01-01"
        report.players.append(
            Player(
                URL = playerURL,
                last_game = last_game
                )
            )
    return report