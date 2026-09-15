import pandas as pd

def getNameAndID(source: str, sourceID: str):

    db = pd.read_csv("_Data/teams.csv")

    for row in db.itertuples(index=False):
        canonical_id, proballersID, flashscoreID, teamName, teamSubtext = row
        if source == "proballers":
            if proballersID == sourceID:
                return teamName, canonical_id
        elif source == "flashscore":
            if flashscoreID == sourceID:
                return teamName, canonical_id
    
    return "0000", "Unknown Team"