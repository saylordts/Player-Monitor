import subprocess

from Change import Change


def overallEdit(allChanges: list[Change]) -> tuple[str, list[Change] | None]:
    errorMessage = ""
    numUpdatedChanges = sum(change.type == "update" for change in allChanges)
    newRowsCheck = not all(change.type == "update" for change in allChanges)
    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        for changeIndex, change in enumerate(allChanges, start=1):
            if changeIndex == 1 and numUpdatedChanges>0: print("UPDATED TEAMS:")
            if changeIndex == numUpdatedChanges and newRowsCheck: print("NEW TEAMS:")
            print(
                f"{changeIndex}. "
                f"{change.teamName} ({change.teamSubtext})"
                f"\n   Canonical ID: {change.canonicalID}"
                f"\n   Proballers ID: {change.proballersUpdateText()}"
                f"\n   Flashscore ID: {change.flashscoreUpdateText()}"
                )

        choice = input("Enter the number of the team you wish to edit (d for done, q to quit)")

        if choice.lower() == "q": return ("quit", None)
        if choice.lower() == "d": return ("done", allChanges)

        if not choice.isdigit():
            errorMessage = "Please enter a valid response."
            continue

        choice = int(choice)
        
        if 1 <= choice <= len(allChanges):
            edit = editOne(allChanges, choice-1)
            if edit[0] == "quit": return ("quit", None)
            allChanges = edit[1]
            continue

        errorMessage = f"{choice} is not in bounds 1-{len(allChanges)}"


def editOne(allChanges: list[Change], changeIndex: int) -> tuple[str, list[Change]]:
    errorMessage = ""
    while True:
        change = allChanges[changeIndex]
        text = (
            f"   Type of Change: "
            f"{change.type}"
            f"\n   Canonical ID: "
            f"{change.canonicalID}"
            f"\n1. "
            f"Team Name: "
            f"{change.teamName}"
            f"\n2. "
            f"Team Subtext: "
            f"{change.teamSubtext}"
        )
        if change.proballersChange(): 
            text += (
                f"\n3."
                f"Proballers ID: "
                f"{change.proballersUpdateText()}"
            )
            if change.flashscoreChange(): 
                text += (
                    f"\n4. "
                    f"Flashscore ID: "
                    f"{change.flashscoreUpdateText()}"
                )
            else:
                text += (
                    f"\n   "
                    f"Flashscore ID: "
                    f"{change.flashscoreUpdateText()}"
                )
        else:
            text += (
                f"\n  "
                f"Proballers ID: "
                f"{change.proballersUpdateText()}"
                f"\n3. "
                f"Flashscore ID: "
                f"{change.flashscoreUpdateText()}"
            )
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print(text)
        print()
        print("Notes: Team Name and Subtext can be edited. Selecting Proballers ID or Flashscore ID will delete this change, and if there are no other changes, this team change will be discarded.")
        choice = input("Enter the number of the value you wish to edit/delete (d for done, x to delete, q to quit)")

        if choice.lower() == "q": return ("quit", allChanges)
        if choice.lower() == "d": return ("done", allChanges)
        
        if choice.lower() == "x":
            allChanges.pop(changeIndex)
            return ("delete", allChanges)

        if not choice.isdigit():
            errorMessage = "Please enter a valid response."
            continue
        
        choice = int(choice)

        if choice == 1:
            rename = input("\nInput New Team Name: ")
            if rename: allChanges[changeIndex].teamName = rename
            continue
        if choice == 2:
            rename = input("\nInput New Team Subtext: ")
            if rename: allChanges[changeIndex].teamSubtext = rename
            continue
        if choice == 3:
            if change.proballersChange():
                if not change.flashscoreChange():
                    check = deleteCheck()
                    if check:
                        allChanges.pop(changeIndex)
                        return ("delete", allChanges)
                    else: continue
                else: 
                    allChanges[changeIndex].newProballersID = None
            elif change.flashscoreChange():
                check = deleteCheck()
                if check:
                    allChanges.pop(changeIndex)
                    return ("delete", allChanges)
                else: continue
        if choice == 4: 
            allChanges[changeIndex].newFlashscoreID = None

def deleteCheck() ->  bool:
    errorMessage = ""
    while True: 
        if errorMessage: print(errorMessage)
        check = input("Removing this ID update may remove the entire team change. Confirm? (Y/n): ")

        if check.lower() == "y": return True
        if check.lower() == "n": return False

        errorMessage = "Please enter Y or N"