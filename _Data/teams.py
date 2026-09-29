import pandas as pd

def getTeamInfo(source: str, sourceID: str, sourceName: str, sourceLink: str):

    # read in saved file
    savedDF = pd.read_csv(
        "_Data/teams.csv",
        dtype={
            "canonicalID": "string",
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )

    # check if team exists in the saved file
    for row in savedDF.itertuples(index=False):
        canonicalID, proballersID, flashscoreID, teamName, teamSubtext = row
        if source == "proballers":
            savedID = proballersID
        elif source == "flashscore":
            savedID = flashscoreID

        if pd.notna(savedID) and savedID == sourceID:
            return canonicalID, teamName, teamSubtext

    # read in temp file
    tempFile = "_Data/tempTeams.csv"
    tempDF = pd.read_csv(
        tempFile,
        dtype={
            "proballersID": "string",
            "flashscoreID": "string"
        }
    )

    # check if team exists in temp file based on source ID
    for row in tempDF.itertuples(index=False):
        teamName, proballersID, flashscoreID, _ = row
        if source == "proballers":
            tempID = proballersID
        elif source == "flashscore":
            tempID = flashscoreID
        if pd.notna(tempID) and tempID == sourceID: return "0000", sourceName+"?", ""

    columns = tempDF.columns.tolist()

    # create new row for unmatched teams
    if source == "proballers":
        new_row = pd.DataFrame([[sourceName, str(sourceID), pd.NA, sourceLink]], columns=columns)
    elif source == "flashscore":
        new_row = pd.DataFrame([[sourceName, pd.NA, str(sourceID), sourceLink]], columns=columns)

    # save to temp file
    tempDF = pd.concat([tempDF, new_row], ignore_index=True)
    tempDF.to_csv(tempFile, index=False)

    return "0000", sourceName+"?", ""