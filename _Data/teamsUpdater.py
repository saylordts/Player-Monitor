import subprocess

import pandas as pd
from rapidfuzz import process, fuzz

def teamsUpdater():
    tempDF = pd.read_csv(
        "_Data/tempTeams.csv",
        dtype={
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )
    savedDF = pd.read_csv(
        "_Data/teams.csv",
        dtype={
            "canonicalID": "string",
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )
    savedDF = tempDF

    for tempRow in tempDF.itertuples(index=False):
        tempTeamName, tempProballersID, tempFlashscoreID = tempRow
        tempID = ""
        selected = None
        noMatches = False

        if not pd.isna(tempProballersID):
            tempID += f"PROBALLERS ID: {tempProballersID}"
        if not pd.isna(tempProballersID) and not pd.isna(tempFlashscoreID): 
            tempID += "; "
        if not pd.isna(tempFlashscoreID):
            tempID += f"FLASHSCORE ID: {tempFlashscoreID}"
        matches = process.extract(
            tempTeamName,
            savedDF["teamName"],
            scorer=fuzz.token_set_ratio,
            limit=5,
            score_cutoff=40
        )

        while True:

            selected = selectMatch(
                tempTeamName, 
                tempID,
                matches,
                savedDF
            )

            if selected == "quit":
                return

            if selected is None:
                noMatches = True
                break

            selected_name, selected_score, selected_index = selected
            selected_team = savedDF.iloc[selected_index]
            proballersUpdateText = selected_team["proballersID"]
            if not pd.isna(tempProballersID):
                proballersUpdateText += f" -> {tempProballersID}"
            flashscoreUpdateText = selected_team["flashscoreID"]
            if not pd.isna(tempFlashscoreID):
                flashscoreUpdateText += f" -> {tempFlashscoreID}"

            confirmed = confirmMatch(
                selected_name,
                tempTeamName,
                proballersUpdateText,
                flashscoreUpdateText
            )

            if not confirmed:
                continue

            if not pd.isna(tempProballersID):
                savedDF.at[
                    selected_index,
                    "proballersID",
                ] = tempProballersID
            if not pd.isna(tempFlashscoreID):
                savedDF.at[
                    selected_index,
                    "flashscoreID",
                ] = tempFlashscoreID

            break
        if noMatches==True:
            print("noMatches")

def selectMatch(tempTeamName, tempID, matches, savedDF):
    errorMessage = ""
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print("============================================================")
        print(f"UNRECOGNIZED TEAM: {tempTeamName}")
        print(tempID)
        print("============================================================")

        for matchIndex, match in enumerate(matches):
            match_name, score, index = match
            team = savedDF.iloc[index]
        
            print(
                "   "
                f"{matchIndex+1}."
                f"  {score:5.1f}%  "
                f"{team['teamName']} "
                # f"({team['canonicalID']})"
            )

        choice = input("\nEnter the number of the correct team (0 for none, q to quit): ")
        
        if choice.lower() == "q":
            return "quit"
        
        if choice == "":
            return matches[0]
        
        if not choice.isdigit():
            errorMessage = "Please enter a number."
            continue
        
        choice = int(choice)
        
        if choice == 0:
            return None
        if 1 <= choice <= len(matches):
            return matches[choice - 1]

        errorMessage = f"{choice} not in bounds 0-{len(matches)}"


def confirmMatch(selected_name, tempTeamName, proballersUpdateText, flashscoreUpdateText):
    errorMessage = ""
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print(f"Saved Name: {selected_name}")
        print(f"Unrecognized Name to Merge: {tempTeamName}")
        print(f"Proballers ID: {proballersUpdateText}")
        print(f"Flashscore ID: {flashscoreUpdateText}")
        choice = input(f"Confirm: Update {selected_name} with these values? (Y/n)")
        
        if choice.lower() == "n": 
            return False
        elif choice.lower() in ["y",""]:
            return True
        else:
            errorMessage = "Please enter Y or N."

if __name__ == "__main__":
    teamsUpdater()