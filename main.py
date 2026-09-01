from _1_Read_In_Players.playerReader import readPlayers
from _2_Run_Scrapers.scraperCommander import scraperCommander
from _3_Write_Report.playerWriter import writeMJML
from _3_Write_Report.mjmlConverter import writeHTML
from _4_Send_Emails.emailSender import sendEmail
from _5_Save_Results.playerSaver import savePlayers

def main(debug=True):
    report = readPlayers()

    report = scraperCommander(report)

    report = writeMJML(report)

    report = writeHTML(report)

    if not debug:
      savePlayers(report)
      sendEmail(report)

main()