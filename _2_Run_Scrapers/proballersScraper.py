import requests
from bs4 import BeautifulSoup
from datetime import datetime
from _2_Run_Scrapers.PlayerScrapeError import PlayerScrapeError
from _DClasses.game import Game
from _DClasses.player import Player, Date_Link
from _DClasses.proballersData import ProballersData
from _DClasses.report import Report

headers = {
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

def findDates(report: Report):
    for playerIndex, player in enumerate(report.players):
        try:
            dates_links = findDateOnePlayer(player.profileLinks["proballers"])
            report.players[playerIndex].found_games.proballers = dates_links
        except requests.RequestException as e:
            errorText += f"Failed to scrape {player.profileLinks['proballers']}: {e}"
            report.errors.append(errorText)
    return report

def findDateOnePlayer(link: str):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        raise
    soup = BeautifulSoup(page.content, "html.parser")
    last_five = soup.find(id="anchor-last5games")
    table_all = last_five.find(
        "table", class_="table"
       )
    table_body = table_all.tbody
    table_rows = table_body.find_all("tr")

    dates_links = []      
    for table_row in table_rows:
        table_drawers = table_row.find_all("td")
                
        game_date = datetime.strptime(table_drawers[0].a.text.strip(), "%b %d, %Y").date()           
        game_link = f"https://www.proballers.com{table_drawers[0].a['href']}"

        dates_links.append(Date_Link(
            date = game_date, 
            link = game_link
        ))

    return dates_links

def scrapeOneGame(link: str, player: Player):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        errorMessage = f"Failed to scrape {link}: {e}"
        raise PlayerScrapeError(errorMessage)

    playerID = player.getProballersID()
    
    soup = BeautifulSoup(page.content, "html.parser")
    team_info = soup.find(
        "div", class_="home-game__content__entry home-game__content__team-stats"
       )
    teams = team_info.div.find_all("div", class_="row")
    home = True
    table_drawers = []
    for teamIndex, team in enumerate(teams):
        rows = team.table.tbody.find_all("tr")
        for row in rows:
            found_href = row.find("td", class_="left first__left d-flex align-items-center").a["href"]
            if playerID in found_href:
                table_drawers = row.find_all("td")
                home = True if teamIndex == 0 else False

    if not table_drawers:
        errorMessage = f"Player {player.name} not found in game {link}"
        raise PlayerScrapeError(errorMessage)

    game_info = soup.find(
        "div", class_="home-game__content__result__final-score__score"
        )
    date = game_info.find("span", class_="date").text.strip()
    score = game_info.find("span", class_="score").text.strip()

    team_info = soup.find(
        "div", class_="home-game__content__result__final-score__content"
    )
    away_team = team_info.find("div", class_="home-game__content__result__final-score__team home-game__content__result__final-score__team--right").h2.a.text.strip()
    home_team = team_info.find("div", class_="home-game__content__result__final-score__team").h2.a.text.strip()
    print(f"Scraping Game {away_team} @ {home_team} for {player.name}")
    table_drawers = [table_drawer.text.strip() for table_drawer in table_drawers]

    game = ProballersData(
        date = date,
        home_team = home_team,
        away_team = away_team,
        score = score,
        home = home,
        pts = table_drawers[1],
        reb = table_drawers[2],
        ast = table_drawers[3],
        min = table_drawers[4],
        twos = table_drawers[5],
        threes = table_drawers[6],
        fg_pct = table_drawers[7].replace("%", "&#37;"),
        fts = table_drawers[8],
        ft_pct = table_drawers[9].replace("%", "&#37;"),
        oreb = table_drawers[10],
        dreb = table_drawers[11],
        to = table_drawers[14],
        stl = table_drawers[15],
        blk = table_drawers[16],
        pfs = table_drawers[17],
        plus_minus = table_drawers[19],
        eff = table_drawers[20]
    ).toGame()

    return game