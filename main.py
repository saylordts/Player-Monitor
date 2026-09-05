from _1_Read_In_Players.playerReader import readPlayers
from _2_Run_Scrapers.scraperCommander import scraperCommander
from _3_Write_Report.writeReport import writeReport
from _4_Send_Emails.emailSender import sendEmail
from _5_Save_Results.playerSaver import savePlayers
import argparse

def main(debug=True):
    report = readPlayers()

    report = scraperCommander(report)

    report = writeReport(report)

    if not debug:
      savePlayers(report)
      sendEmail(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )
    args = parser.parse_args()

    main(debug=not args.no_debug)