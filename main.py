from proballersScraper import proballersScraper
from playerReadScript import readPlayers
from playerWriter import writeMJML
from mjmlConverter import writeHTML
from emailSender import sendEmail
from player import Player
from game import Game
from report import Report

report = readPlayers()

report = proballersScraper(report)

report = writeMJML(report)

report = writeHTML(report)

sendEmail(report)