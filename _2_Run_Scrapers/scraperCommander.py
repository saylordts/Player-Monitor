from _DClasses.report import Report
import _2_Run_Scrapers.flashscoreScraper as fs
import _2_Run_Scrapers.proballersScraper as pb
from _1_Read_In_Players.playerReader import readPlayers


def scraperCommander(report: Report):
    flashscoreDates = fs.findDates(report)
    proballersDates = pb.findDates(report)
    skimmed_fs_dates = dateSkimmer(report, flashscoreDates)
    skimmed_pb_dates = dateSkimmer(report, proballersDates)

    playersData = chooseSource(skimmed_fs_dates, skimmed_pb_dates)

    report = runScrapers(report, playersData)
    return report


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

def runScrapers(report: Report, playersData: list):
    for player_data in playersData:
        player_name = player_data["name"]
        playerIndex = report.getPlayerIndexByName(player_name)
        for date_link in player_data["dates_links"]:
            if date_link["source"] == "flashscore":
                game = fs.scrapeOneGame(date_link["link"], report.players[playerIndex])
                if game:
                    report.players[playerIndex].games.append(game)
            elif date_link["source"] == "proballers":
                game = pb.scrapeOneGame(date_link["link"],report.players[playerIndex])
                if game:
                    report.players[playerIndex].games.append(game)
    return report