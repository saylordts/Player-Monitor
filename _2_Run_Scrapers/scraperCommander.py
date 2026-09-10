from _DClasses.report import Report
import _2_Run_Scrapers.flashscoreScraper as fs
import _2_Run_Scrapers.proballersScraper as pb


def scraperCommander(report: Report):
    report = fs.findDates(report)
    report = pb.findDates(report)
    
    for playerIndex, player in enumerate(report.players):
        report.players[playerIndex] = player.chooseDates()

    report = runScrapers(report)

    return report


def runScrapers(report: Report):
    for playerIndex, player in enumerate(report.players):
        for use_game in player.use_games:
            if "flashscore" in use_game.link:
                try:
                    game = fs.scrapeOneGame(use_game.link, report.players[playerIndex])
                    if game:
                        report.players[playerIndex].games.append(game)
                except PlayerScrapeError as e:
                    report.errors.append(e)
            elif "proballers" in use_game.link:
                try:
                    game = pb.scrapeOneGame(use_game.link,report.players[playerIndex])
                    if game:
                        report.players[playerIndex].games.append(game)
                except PlayerScrapeError as e:
                    report.errors.append(e)
    return report

class PlayerScrapeError(Exception):
    pass