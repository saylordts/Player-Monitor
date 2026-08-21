from DClasses.report import Report
import flashscoreScraper as fs
import proballersScraper as pb
from playerReader import readPlayers


report = readPlayers()

def runScrapers(report: Report):
    flashscoreDates = fs.findDates(report)
    proballersDates = pb.findDates(report)
    for player_data in proballersDates:
        print (f"Player: {player_data['name']}")
        print("\n")
        for game in player_data["dates_links"]:
            print(f"Date: {game['date']}, Link: {game['link']}")
        print("\n \n")