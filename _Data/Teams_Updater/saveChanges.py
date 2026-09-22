import pandas as pd
from Change import Change


def saveChanges(savedDF: pd.DataFrame, allChanges: list[Change]):

    columns = savedDF.columns.tolist()
    for change in allChanges:
        if change.type == "new":
            newID = getNextCanonicalID(savedDF)
            new_row = pd.DataFrame([[newID, change.newProballersID, change.newFlashscoreID, change.teamName, change.teamSubtext]], columns=columns)
            savedDF = pd.concat([savedDF, new_row], ignore_index=True)
        else:
            if change.proballersChange():
                savedDF.loc[savedDF['canonicalID'] == change.canonicalID, "proballersID"] = change.newProballersID
            if change.flashscoreChange():
                savedDF.loc[savedDF['canonicalID'] == change.canonicalID, "flashscoreID"] = change.newFlashscoreID

    return savedDF

def getNextCanonicalID(savedDF):
    if savedDF.empty: return "0001"

    existingIds = pd.to_numeric(
        savedDF["canonicalID"],
        errors="coerce"
    ).dropna()

    if existingIds.empty:
        return "0001"

    nextID = int(existingIds.max()) + 1

    return f"{nextID:04d}"