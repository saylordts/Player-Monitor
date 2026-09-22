import pandas as pd

def getTeamInfo(source: str, sourceID: str, sourceName: str):

    savedDF = pd.read_csv(
        "_Data/teams.csv",
        dtype={
            "canonicalID": "string",
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )

    for row in savedDF.itertuples(index=False):
        canonicalID, proballersID, flashscoreID, teamName, teamSubtext = row
        if source == "proballers":
            savedID = proballersID
        elif source == "flashscore":
            savedID = flashscoreID

        if pd.notna(savedID) and savedID == sourceID:
            return canonicalID, teamName, teamSubtext

    tempFile = "_Data/tempTeams.csv"
    tempDF = pd.read_csv(
        tempFile,
        dtype={
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )

    for row in tempDF.itertuples(index=False):
        teamName, proballersID, flashscoreID = row
        if source == "proballers":
            tempID = proballersID
        elif source == "flashscore":
            tempID = flashscoreID
        if pd.notna(tempID) and tempID == sourceID: return "0000", sourceName+"?", ""

    columns = tempDF.columns.tolist()

    for row in tempDF.itertuples(index=False):
        teamName, proballersID, flashscoreID = row
        if sourceName == teamName:
            if source == "proballers" and pd.isna(proballersID):
                tempDF.loc[tempDF['teamName'] == sourceName, "proballersID"] = sourceID
                tempDF.to_csv(tempFile, index=False)
            elif source == "flashscore" and pd.isna(flashscoreID):
                tempDF.loc[tempDF['teamName'] == sourceName, "flashscoreID"] = sourceID
                tempDF.to_csv(tempFile, index=False)
            return "0000", sourceName+"?", ""

    if source == "proballers":
        new_row = pd.DataFrame([[sourceName, str(sourceID), pd.NA]], columns=columns)
    elif source == "flashscore":
        new_row = pd.DataFrame([[sourceName, pd.NA, str(sourceID)]], columns=columns)
    tempDF = pd.concat([tempDF, new_row], ignore_index=True)

    tempDF.to_csv(tempFile, index=False)
    return "0000", sourceName+"?", ""