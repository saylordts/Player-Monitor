import pandas as pd

def savePlayers(report):
    df = pd.read_csv("_Data/playerLinks.csv")
    columns = df.columns.tolist()
    for player in report.players:
        last_game = max([game.date for game in player.games])
        matching_row = df[df["name"] == player.name]
        if not matching_row.empty:
            print(f"Updating last game for {player.name} to {last_game.isoformat()}")
            df.loc[df['name'] == player.name, "Last Played"] = last_game.isoformat()
        else:
            new_row = pd.DataFrame([[player.name, last_game.isoformat()]], columns=columns)
            df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("_Data/players.csv", index=False)