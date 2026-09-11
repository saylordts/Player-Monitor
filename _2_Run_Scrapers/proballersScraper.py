import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
            dates_links, player_team = findDateOnePlayer(player.profileLinks["proballers"])
            report.players[playerIndex].found_games.proballers = dates_links
            report.players[playerIndex].team = player_team
        except requests.RequestException as e:
            errorText += f"Failed to scrape {player.profileLinks['proballers']}: {e}"
            report.errors.append(errorText)
    return report

def findDateOnePlayer(link: str):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
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

    player_team = soup.find("div", class_="banner__biography__content").p.a.text

    return dates_links, player_team

def scrapeOneGame(link: str, player: Player):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        raise
    soup = BeautifulSoup(page.content, "html.parser")
    team_info = soup.find(
        "div", class_="home-game__content__entry home-game__content__team-stats"
       )
    teams = team_info.div.find_all("div", class_="row")
    home = True
    for teamIndex, team in enumerate(teams):
        rows = team.table.tbody.find_all("tr")
        for row in rows:
            row_player = row.find("td", class_="left first__left d-flex align-items-center").a.text.strip()
            if row_player == player.name:
                table_drawers = row.find_all("td")
                home = True if teamIndex == 0 else False

    if table_drawers == []:
        print(f"Player {player.name} not found in game {link}")
        return None

    game_info = soup.find(
        "div", class_="home-game__content__result__final-score__score"
        )
    date = game_info.find("span", class_="date").text.strip()
    score = game_info.find("span", class_="score").text.strip()

    team_info = soup.find(
        "div", class_="home-game__content__result__final-score__content"
    )
    team_arg = "home-game__content__result__final-score__team home-game__content__result__final-score__team--right" if home else "home-game__content__result__final-score__team"
    opp_team = team_info.find("div", class_=team_arg).h2.a.text.strip()

    table_drawers = [table_drawer.text.strip() for table_drawer in table_drawers]

    game = ProballersData(
        date = date,
        opp_team = opp_team,
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