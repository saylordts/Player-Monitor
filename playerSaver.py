import pandas as pd

def savePlayers(report):
    df = pd.read_csv("Data/players.csv")
    columns = df.columns.tolist()
    for player in report.players:
        last_game = max([game.date for game in player.games])
        matching_row = df[df["URL"] == player.URL]
        if not matching_row.empty:
            print(f"Updating last game for {player.name} to {last_game.isoformat()}")
            df.loc[df['URL'] == player.URL, "Last Played"] = last_game.isoformat()
        else:
            new_row = pd.DataFrame([[player.URL, last_game.isoformat()]], columns=columns)
            df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("Data/players.csv", index=False)