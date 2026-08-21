from re import match

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from DClasses.game import Game
from DClasses.player import Player
from DClasses.report import Report
import json

dateHeaders = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
gameHeaders = {
    "Referer": "https://www.flashscore.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-fsign": "SW9D1eZo",
}

def findDates(report: Report):
    players_data = []
    for player in report.players:
        player_data = findDatesOnePlayer(player.links["flashscore"])
        player_data["name"] = player.name
        players_data.append(player_data)

    return players_data

def findDatesOnePlayer(link: str):
    try:
        page = requests.get(link, headers=dateHeaders, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        return {"dates_links": {} }
    soup = BeautifulSoup(page.content, "html.parser")
    for script in soup.find_all("script"):
        if "playerProfilePageEnvironment" in script.text:
            data = script.text
            break

    json_text = data.split("window.playerProfilePageEnvironment = ")[1]
    json_text = json_text.split(";\n")[0]
    player_data = json.loads(json_text)
    last_matches = player_data["lastMatchesData"]["lastMatches"][:5]

    dates_links = []
    for match in last_matches:
        dates_links.append({
            "date": datetime.strptime(match["eventStartTime"], "%d.%m.%y").date(),
            "link": f"https://www.flashscore.com/match/basketball/{match["homeParticipantUrl"]}-{match["homeParticipantEncodedId"]}/{match["awayParticipantUrl"]}-{match["awayParticipantEncodedId"]}/?mid={match["eventEncodedId"]}"
        })
    player_data = {
        "dates_links": dates_links
        }

    return player_data


gameUrl = "https://global.flashscore.ninja/2/x/feed/df_psn_1_GrYesG1t" # INPUT
playerName = "Saylor D." # INPUT

def flashscoreGameScraper():
    try:
        page = requests.get(gameUrl, headers=gameHeaders, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {gameUrl}: {e}")
    allPlayers = page.text.split("PA÷")[1]
    playerList = allPlayers.split("PJ÷")[1:]
    player = next((p for p in playerList if playerName in p), None)
    stats = player.split("PC÷")[1].split("¬~")[0].split("|")
    print(stats)
    pts = stats[0]
    reb = stats[1]
    ast = stats[2]
    min = stats[3]
    fgm = stats[4]
    fga = stats[5]
    twosm = stats[6]
    twosa = stats[7]
    threesm = stats[8]
    threesa = stats[9]
    ftm = stats[10]
    fta = stats[11]
    plusminus = stats[12]
    oreb = stats[13]
    dreb = stats[14]
    fouls = stats[15]
    steals = stats[16]
    turnovers = stats[17]
    blk = stats[18]