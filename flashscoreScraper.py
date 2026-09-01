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
            #"link": f"https://2.flashscore.ninja/2/x/feed/df_psn_1_{match['eventEncodedId']}"
            "link": f"https://www.flashscore.com/match/basketball/{match["homeParticipantUrl"]}-{match["homeParticipantEncodedId"]}/{match["awayParticipantUrl"]}-{match["awayParticipantEncodedId"]}/summary/player-stats/overall/?mid={match["eventEncodedId"]}"
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
    
    playerID = player.links["flashscore"].split("/")[-1]
    allPlayers = playerPage.text.split("PA÷")[1]
    playerList = allPlayers.split("PJ÷")[1:]
    playerdata = next((p for p in playerList if playerID in p), None)
    stats = playerdata.split("PC÷")[1].split("¬~")[0].split("|")

    soup = BeautifulSoup(basicPage.content, "html.parser")
    title = soup.find("title").text
    unf_date = title.split(",")[0][-10:]
    game_date_form = datetime.strptime(unf_date, "%d/%m/%Y").date()
    versus_text = title.split(",")[0][:-11].strip()

    return Game(
            date = game_date_form,
            versus_text = versus_text,
            win_loss = "NEED WIN/LOSS",
            score = "NEED SCORE",
            pts = stats[0],
            reb = stats[1],
            ass = stats[2],
            mins = stats[3],
            twos = f"{stats[6]} - {stats[7]}",
            threes = f"{stats[8]} - {stats[9]}",
            fg_pct = "NEED FG%",
            fts = f"{stats[10]} - {stats[11]}",
            ft_pct = "NEED FT%",
            oreb = stats[13],
            dreb = stats[14],
            stl = stats[16],
            to = stats[17],
            blk = stats[18],
            pfs = stats[15],
            plus_minus = stats[12],
            eff = "NEED EFF"
            )
