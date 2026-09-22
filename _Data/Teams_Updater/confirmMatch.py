import subprocess

import Change


def confirmMatch(change: Change, tempTeamName: str):
    errorMessage = ""
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print(f"Saved Name: {change.teamName}")
        print(f"Unrecognized Name to Merge: {tempTeamName}")
        print(f"Proballers ID: {change.proballersUpdateText()}")
        print(f"Flashscore ID: {change.flashscoreUpdateText()}")
        choice = input(f"Confirm: Update {change.teamName} with these values? (Y/n)")
        
        if choice.lower() == "n": 
            return False
        if choice.lower() in ["y",""]:
            return True
        errorMessage = "Please enter Y or N."