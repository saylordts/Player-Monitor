import pandas as pd
from rapidfuzz import process, fuzz

from confirmMatch import confirmMatch
from newRow import newRow
from selectMatch import selectMatch
from Change import Change


def updateRow(tempRow, savedDF) -> tuple[str, Change | None]: 
    tempTeamName, tempProballersID, tempFlashscoreID = tempRow
    tempID = ""
    
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
        score_cutoff=60
    )

    while True:
        selected = selectMatch(
            tempTeamName, 
            tempID,
            matches,
            savedDF
        )
    
        if selected[0] == "quit":
            return ("quit", None)

        if selected[0] == "skip":
            return ("skip", None)
    
        if selected[1] is None:
            break
    
        selected_name, selected_score, selected_index = selected[1]
        selected_team = savedDF.iloc[selected_index]
        change = Change(
            type="update",
            teamName=selected_name,
            canonicalID=selected_team["canonicalID"],
            oldProballersID=selected_team["proballersID"],
            oldFlashscoreID=selected_team["flashscoreID"],
            teamSubtext=selected_team["teamSubtext"]
        )
        if not pd.isna(tempFlashscoreID):
            change.newFlashscoreID = tempFlashscoreID
        if not pd.isna(tempProballersID):
            change.newProballersID = tempProballersID
    
        confirmed = confirmMatch(change,tempTeamName)
    
        if not confirmed:
            continue

        return ("update", change)
    return newRow(tempRow,tempID)