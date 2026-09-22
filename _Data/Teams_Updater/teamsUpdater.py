import subprocess

import pandas as pd

from consolidateTempDF import consolidateTempDF
from saveChanges import saveChanges
from updateRow import updateRow
from overallEdit import overallEdit
from Change import Change

def teamsUpdater():
    tempDF = pd.read_csv(
        "_Data/tempTeams.csv",
        dtype={
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )
    savedFile = "_Data/teams.csv"
    savedDF = pd.read_csv(
        savedFile,
        dtype={
            "canonicalID": "string",
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )

    allChanges: list[Change] = []

    tempDF = consolidateTempDF(tempDF)

    for tempRow in tempDF.itertuples(index=False):
        update = updateRow(tempRow,savedDF)
        if update[0] == "quit": return
        if update[0] == "skip": continue
        allChanges.append(update[1])
    if not allChanges: return

    errorMessage = ""

    while True:
        updatedRows: list[Change] = []
        newRows: list[Change] = []

        for change in allChanges:
            if change.type == "update": updatedRows.append(change)
            if change.type == "new": newRows.append(change)

        subprocess.run("cls", shell=True)

        print("============================================================")
        print("FINAL REVIEW")
        print("============================================================")
        print()
        if updatedRows: 
            print("UPDATED TEAMS:")
            for changeIndex, change in enumerate(updatedRows, start=1):
                print(
                    f"{changeIndex}. "
                    f"{change.teamName} ({change.teamSubtext})"
                    f"\n   Canonical ID: {change.canonicalID}"
                    f"\n   Proballers ID: {change.proballersUpdateText()}"
                    f"\n   Flashscore ID: {change.flashscoreUpdateText()}"
                    )
                print()
            print()

        if newRows: 
            print("NEW TEAMS:")
            for changeIndex, change in enumerate(newRows, start=1):
                print(
                    f"{changeIndex}. "
                    f"{change.teamName} ({change.teamSubtext})"
                    f"\n   Proballers ID: {change.proballersUpdateText()}"
                    f"\n   Flashscore ID: {change.flashscoreUpdateText()}"
                    )

        if errorMessage: print(errorMessage)
        
        print("Key Binds: y for yes, n for no (quit), e for edit")
        choice = input("\nSave these changes? (Y/n/e): ")   

        if choice.lower() in ["y", ""]:
            savedDF = saveChanges(savedDF, allChanges)
            savedDF.to_csv(savedFile, index=False) 
            return

        if choice.lower() == "n": return

        if choice.lower() == "e":
            editResults = overallEdit(allChanges)
            if editResults[0] == "quit": return
            allChanges = editResults[1]
            continue

        errorMessage = "Please enter Y, N, or E."


if __name__ == "__main__":
    teamsUpdater()