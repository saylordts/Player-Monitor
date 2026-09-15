import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

playerUpdateFile = Path(
    os.getenv("PLAYER_UPDATE_FILE", "_Data/players.csv")
) 

def savePlayers(report):
    df = pd.read_csv(playerUpdateFile)
    columns = df.columns.tolist()
    for player in report.players:
        if player.games:
            last_game = max([game.date for game in player.games])
            matching_row = df[df["name"] == player.name]
            if not matching_row.empty:
                df.loc[df['name'] == player.name, "lastPlayed"] = last_game.isoformat()
            else:
                new_row = pd.DataFrame([[player.name, last_game.isoformat()]], columns=columns)
                df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(playerUpdateFile, index=False) 