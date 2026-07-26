from DClasses.report import Report
import flashscoreScraper as fs
from playerReader import readPlayers


report = readPlayers()

def runScrapers(report: Report):
    flashscoreDates = fs.findDates(report)
    for date in flashscoreDates:
        print(date)