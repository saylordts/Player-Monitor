import subprocess

import pandas as pd


from rapidfuzz import process, fuzz


def consolidateTempDF(tempDF: pd.DataFrame) -> pd.DataFrame:
    while True:
        changed = False
        for tempRow in tempDF.itertuples():
            tempIndex, tempTeamName, _, _ = tempRow 
            matches = process.extract(
                tempTeamName,
                tempDF["teamName"],
                scorer=fuzz.token_set_ratio,
                limit=5,
                score_cutoff=60
            )
            matches = [
                match for match in matches
                if match[2] != tempIndex
            ]
            if not matches: continue
            chooseResults = chooseMatch(tempRow, matches, tempDF)
            if chooseResults[0] == "none": continue
            if chooseResults[0] == "quit": return ("quit", tempDF)
            if chooseResults[0] == "complete":
                tempDF = chooseResults[1]
                changed = True
                break
        if not changed: return tempDF


def chooseMatch(tempRow, matches, tempDF):
    _, tempTeamName, tempProballersID, tempFlashscoreID = tempRow 
    tempIdText = f"Proballers ID: {tempProballersID}" if not pd.isna(tempProballersID) else f"Flashscore ID: {tempFlashscoreID}"
    errorMessage = ""
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print(f"Matches found for {tempTeamName} ({tempIdText})")
        print()
        for matchIndex, match in enumerate(matches, start=1):
            _, score, dfIndex = match
            team = tempDF.iloc[dfIndex]
            idText = f"Proballers ID: {team['proballersID']}" if not pd.isna(team['proballersID']) else f"Flashscore ID: {team['flashscoreID']}"
            print(
                f"{matchIndex}."
                f"{team["teamName"]}"
                f"{idText}"
                f"Score: {score}"
            )

        choice = input("\nSelect team to merge (Enter or 0 for none, q to quit): ")

        if choice in ("","0"): return ("none", tempDF)
        if choice.lower() == "q": return("quit", tempDF)

        if not choice.isdigit(): 
            errorMessage = "Please enter a number"
            continue

        choice = int(choice)

        if 1 <= choice <= len(matches):
            combineResults = combineMatch(tempRow, matches[choice-1], tempDF)
            if combineResults[0] == "quit": return("quit", tempDF)
            return ("complete", combineResults[1])

def combineMatch(originalRow, newMatch, tempDF:pd.DataFrame):
    originalIndex, originalTeamName, originalProballersID, originalFlashscoreID = originalRow
    _, _, matchIndex = newMatch
    matchTeamName, matchProballersID, matchFlashscoreID = tempDF.iloc[matchIndex]
    errorMessage = ""
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print(
            f"1. {originalTeamName}"
            f"2. {matchTeamName}"
            )
        choice = input("Select Team Name to Choose (1/2, q to quit)")

        if choice.lower() == "q": return ("quit", tempDF)

        if choice == "1": teamName = originalTeamName; break
        if choice == "2": teamName = matchTeamName; break

        errorMessage = "Please input a valid response"

    proballersID = originalProballersID if not pd.isna(originalProballersID) else matchProballersID
    flashscoreID = originalFlashscoreID if not pd.isna(originalFlashscoreID) else matchFlashscoreID

    tempDF = tempDF.drop(index=[matchIndex, originalIndex])
    
    columns = tempDF.columns.tolist()
    newRow = pd.DataFrame([[teamName,proballersID,flashscoreID]],columns=columns)
    tempDF = pd.concat([tempDF, newRow], ignore_index=True)
    return ("complete", tempDF)
