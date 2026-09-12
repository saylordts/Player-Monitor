import pandas as pd

def savePlayers(report):
    df = pd.read_csv("_Data/playerLinks.csv")
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
    df.to_csv("_Data/playerLinks.csv", index=False)