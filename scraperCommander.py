from DClasses.report import Report
import flashscoreScraper as fs
from playerReader import readPlayers


report = readPlayers()

def runScrapers(report: Report):
    flashscoreDates = fs.findDates(report)
    for player_dates in flashscoreDates:
        for date, link in player_dates.items():
            print(f"Date: {date}, Link: {link}")
        print("\n")