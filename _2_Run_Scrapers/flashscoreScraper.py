import requests
from bs4 import BeautifulSoup
from datetime import datetime
from _DClasses.flashscoreData import FlashscoreData
from _DClasses.game import Game
from _DClasses.player import Player
from _DClasses.report import Report
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
headers = {
    "accept": "*/*",
    "origin": "https://www.flashscore.com",
    "referer": "https://www.flashscore.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/152.0.0.0 Safari/537.36",
    "x-fsign": "SW9D1eZo",
}

def findDates(report: Report):
    players_data = []
    errors = []
    for player in report.players:
        try:
            player_data = findDatesOnePlayer(player.links["flashscore"])
            player_data["name"] = player.name
            players_data.append(player_data)
        except ValueError:
            errors.append(player)

    return players_data, errors

def findDatesOnePlayer(link: str):
    try:
        page = requests.get(link, headers=dateHeaders, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        raise ValueError()
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
            "link": f"https://www.flashscore.com/match/basketball/{match['homeParticipantUrl']}-{match['homeParticipantEncodedId']}/{match['awayParticipantUrl']}-{match['awayParticipantEncodedId']}/summary/player-stats/overall/?mid={match['eventEncodedId']}"
        })
    player_data = {
        "dates_links": dates_links
        }

    return player_data

def scrapeOneGame(link: str, player: Player):
    try:
        basicPage = requests.get(link, headers=gameHeaders, timeout=20)
        basicPage.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        return None
    try:
        matchID = link.split("mid=")[1]
        data_link = f"https://2.flashscore.ninja/2/x/feed/df_psn_1_{matchID}"
        playerPage = requests.get(data_link, headers=gameHeaders, timeout=20)
        playerPage.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        return None
    playerID = player.links["flashscore"].split("/")[-2]
    allPlayers = playerPage.text.split("PA÷")
    homePlayers = allPlayers[2].split("PJ÷")[1:]
    awayPlayers = allPlayers[3].split("PJ÷")[1:]

    playerdata = next((p for p in homePlayers if playerID in p), None)
    if playerdata is None:
        home = False
        playerdata = next((p for p in awayPlayers if playerID in p), None)
    else: 
        home = True
    stats = playerdata.split("PC÷")[1].split("¬~")[0].split("|")

    soup = BeautifulSoup(basicPage.content, "html.parser")

    title = soup.find("title").text
    date = title.split(",")[0][-10:]
    versus_text = title.split(",")[0][:-11].strip()

    title_score = soup.find(
       "meta", property="og:title"
        )
    score = title_score["content"].rsplit(" ", 1)[-1]

    game = FlashscoreData(
        pts = stats[0],
        reb = stats[1],
        ast = stats[2],
        min = stats[3],
        fgMade = stats[4],
        fgAtt = stats[5],
        twosMade = stats[6],
        twosAtt = stats[7],
        threesMade = stats[8],
        threesAtt = stats[9],
        ftMade = stats[10],
        ftAtt = stats[11],
        plus_minus = stats[12],
        oreb = stats[13],
        dreb = stats[14],
        pfs = stats[15],
        stl = stats[16],
        to = stats[17],
        blk = stats[18],
        blka = stats[19],
        date = date,
        versus_text = versus_text,
        score = score,
        home = home
    ).toGame()

    return game
