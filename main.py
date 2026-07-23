from proballersScraper import proballersScraper
from playerReadScript import readPlayers
from playerWriter import writeMJML
from mjmlConverter import writeHTML
from emailSender import sendEmail

report = readPlayers()

report = proballersScraper(report)

report = writeMJML(report)

report = writeHTML(report)

sendEmail(report)