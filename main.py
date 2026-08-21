from playerSaver import savePlayers
from playerReader import readPlayers
from playerWriter import writeMJML
from mjmlConverter import writeHTML
from emailSender import sendEmail
from scraperCommander import scraperCommander


def main(debug=True):
    report = readPlayers()

    report = scraperCommander(report)
    
    # report = proballersScraper(report)

    # report = writeMJML(report)

    # report = writeHTML(report)

    # savePlayers(report)

    # if not debug:
    #   sendEmail(report)

main()