import subprocess


def selectMatch(tempTeamName, tempID, matches, savedDF):
    errorMessage = ""

    if not matches: return ("none found", None)

    while True:
        subprocess.run("cls", shell=True)
        if errorMessage: print(errorMessage)
        print("============================================================")
        print(f"UNRECOGNIZED TEAM: {tempTeamName}")
        print(tempID)
        print("============================================================")

        for matchIndex, match in enumerate(matches):
            _, score, index = match
            team = savedDF.iloc[index]
        
            print(
                "   "
                f"{matchIndex+1}."
                f"  {score:5.1f}%  "
                f"{team['teamName']} "
                f"({team['canonicalID']})"
            )

        choice = input("\nEnter the number of the correct team (0 for none, q to quit, s to skip): ")
        
        if choice.lower() == "q":
            return ("quit", None)

        if choice.lower() == "s":
            return ("skip", None)
        
        if choice == "":
            return ("found", matches[0])
        
        if not choice.isdigit():
            errorMessage = "Please enter a number."
            continue
        
        choice = int(choice)
        
        if choice == 0:
            return ("none selected", None)
        if 1 <= choice <= len(matches):
            return ("found", matches[choice - 1])

        errorMessage = f"{choice} not in bounds 0-{len(matches)}"