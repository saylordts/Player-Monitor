import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
from _2_Run_Scrapers.PlayerScrapeError import PlayerScrapeError
from _DClasses.player import Player, Date_Link
from _DClasses.proballersDataClasses import ProballersGame
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
    in_github_actions = os.getenv("GITHUB_ACTIONS") == "true"

    if in_github_actions:
        player_iterator = report.players
        print("        • Proballers - finding dates...")
    else:
        player_iterator = tqdm(
                    report.players, 
                    desc="• Proballers - finding dates", 
                    unit="player", 
                    bar_format="        {desc}:   {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
                    )

    for playerIndex, player in enumerate(player_iterator):
        link = player.playerData.proballers.getProfileLink()
        try:
            dates_links = findDateOnePlayer(link)
            report.players[playerIndex].found_games.proballers = dates_links
        except requests.RequestException as e:
            errorText = f"Failed to scrape {link}: {e}"
            report.errors.append(errorText)

    if in_github_actions:
        num_dates_found = sum(len(player.found_games.proballers) for player in report.players)
        print(f"          • Proballers - finding dates... DONE ({num_dates_found} games found for {len(report.players)} players)")

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
    print(link)
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        errorMessage = f"Failed to scrape {link}: {e}"
        raise PlayerScrapeError(errorMessage)
    
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
            if player.playerData.proballers.id in found_href:
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
    awayID = team_info.find("div", class_="home-game__content__result__final-score__team home-game__content__result__final-score__team--right").h2.a.text.strip()
    homeID = team_info.find("div", class_="home-game__content__result__final-score__team").h2.a.text.strip()
    
    table_drawers = [table_drawer.text.strip() for table_drawer in table_drawers]

    game = ProballersGame(
        date = date,
        homeID = homeID,
        awayID = awayID,
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