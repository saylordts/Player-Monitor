import subprocess

import pandas as pd

from Change import Change


def newRow(tempRow,tempID):
    tempTeamName, tempProballersID, tempFlashscoreID = tempRow

    subprocess.run("cls", shell=True)

    print("============================================================")
    print(f"UNRECOGNIZED TEAM: {tempTeamName}")
    print(tempID)
    print("============================================================")
    print(f"No accepted matches; creating new saved team")

    print("Key Binds: Enter to accept above name; q to quit, s to skip")
    saveName = input("\nEnter team name to display: ")

    if saveName.lower() == "q": return ("quit", None)
    if saveName.lower() == "s": return ("skip", None)
    if saveName == "": saveName = tempTeamName

    subprocess.run("cls", shell=True)
    
    print("============================================================")
    print(f"NEW TEAM: {saveName}")
    print(tempID)
    print("============================================================")
    print("Key Binds: Enter to leave blank; q to quit, s to skip")

    saveSubtext = input("\n Enter team subtext (country and league): ")

    if saveSubtext.lower() == "q": return ("quit", None)
    if saveSubtext.lower() == "s": return ("skip", None)


    newProballersID = None if pd.isna(tempProballersID) else str(tempProballersID)
    newFlashscoreID = None if pd.isna(tempFlashscoreID) else str(tempFlashscoreID)
    change = Change(
        type="new",
        teamName=saveName,
        newProballersID=newProballersID,
        newFlashscoreID=newFlashscoreID,
        teamSubtext=saveSubtext
    )
    return ("new", change)