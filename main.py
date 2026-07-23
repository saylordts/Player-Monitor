from playerSaver import savePlayers
from proballersScraper import proballersScraper
from playerReader import readPlayers
from playerWriter import writeMJML
from mjmlConverter import writeHTML
from emailSender import sendEmail


def main(debug=False):
    report = readPlayers()

    report = proballersScraper(report)

    report = writeMJML(report)

    report = writeHTML(report)

    savePlayers(report)
    if not debug:
      sendEmail(report)

main(True)