from proballersScraper import proballersScraper
from playerReadScript import readPlayers
from playerWriter import writeMJML
from mjmlConverter import writeHTML
from emailSender import sendEmail


def main(debug=False):
    report = readPlayers()

    report = proballersScraper(report)

    report = writeMJML(report)

    report = writeHTML(report)

    if not debug:
      sendEmail(report)

main()