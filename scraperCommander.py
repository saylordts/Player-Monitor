from DClasses.report import Report
import flashscoreScraper as fs
import proballersScraper as pb
from playerReader import readPlayers


def runScrapers(report: Report):
    flashscoreDates = fs.findDates(report)
    proballersDates = pb.findDates(report)
    skimmed_fs_dates = dateSkimmer(report, flashscoreDates)
    skimmed_pb_dates = dateSkimmer(report, proballersDates)

    playersData = chooseSource(skimmed_fs_dates, skimmed_pb_dates)
    


def dateSkimmer(report: Report, playersData: list):
    for player_data in playersData:
        player_name = player_data["name"]
        cutoff_date = report.getPlayerByName(player_name).last_game
        kept_dates = [date for date in player_data["dates_links"] if date["date"] > cutoff_date]
        player_data["dates_links"] = kept_dates
    return playersData

def chooseSource(FSData: list, PBData: list):
    playersData = []
    for fsData, pbData in zip(FSData, PBData):
        playerData = pbData["dates_links"]
        for playerdata in playerData:
            playerdata["source"] = "proballers"
        for date_link in fsData["dates_links"]:
            if date_link not in playerData:
                date_link["source"] = "flashscore"
                playerData.append(date_link)
        playerData.sort(key=lambda x: x["date"])
        playersData.append({"name": pbData["name"], "dates_links": playerData})
    return playersData
        


