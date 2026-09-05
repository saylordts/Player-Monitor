import requests
from bs4 import BeautifulSoup
from datetime import datetime
from _DClasses.game import Game
from _DClasses.player import Player
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
    players_data = []
    for player in report.players:
        player_data = findDateOnePlayer(player.links["proballers"])
        player_data["name"] = player.name
        players_data.append(player_data)

    return players_data

def findDateOnePlayer(link: str):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        return
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

        dates_links.append({"date": game_date, "link": game_link})

    player_data = {
        "dates_links": dates_links
    }

    return player_data

def scrapeOneGame(link: str, player: Player):
    try:
        page = requests.get(link, headers=headers, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to scrape {link}: {e}")
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    team_info = soup.find(
        "div", class_="home-game__content__entry home-game__content__team-stats"
       )
    teams = team_info.div.find_all("div", class_="row")
    home = True
    table_drawers = []
    for team in teams:
        table = team.table.tbody
        rows = table.find_all("tr")
        for row in rows:
            row_player = row.find("td", class_="left first__left d-flex align-items-center").a.text.strip()
            if row_player == player.name:
                table_drawers = row.find_all("td")
                break
        home = False
    if table_drawers == []:
        print(f"Player {player.name} not found in game {link}")
        return None

    game_info = soup.find(
        "div", class_="home-game__content__result__final-score__score"
        )
    unf_date = game_info.find("span", class_="date").text.strip()
    score = game_info.find("span", class_="score").text.strip()
    score_split = score.split("-")

    if home:
        if score_split[0] > score_split[1]:
            win_loss = "W"
    elif score_split[1] > score_split[0]:
            win_loss = "W"
    else:
        win_loss = "L"

    team_info = soup.find(
        "div", class_="home-game__content__result__final-score__content"
    )
    if home:
        opp_name = team_info.find(
        "div", class_="home-game__content__result__final-score__team"
        ).h2.a.text.strip()
        versus_text = f"@ {opp_name}"
    else:
        opp_name = team_info.find(
        "div", class_="home-game__content__result__final-score__team home-game__content__result__final-score__team--right"
        ).h2.a.text.strip()
        versus_text = f"vs {opp_name}"

    game_date_form = datetime.strptime(unf_date, "%b %d, %Y").date()

    return Game(
            date = game_date_form,
            versus_text = versus_text,
            win_loss = win_loss,
            score = score,
            pts = table_drawers[2].text.strip(),
            reb = table_drawers[3].text.strip(),
            ast = table_drawers[4].text.strip(),
            mins = table_drawers[5].text.strip(),
            twos = table_drawers[6].text.strip(),
            threes = table_drawers[7].text.strip(),
            fg_pct = table_drawers[8].text.strip().replace("%", "&#37;"),
            fts = table_drawers[9].text.strip(),
            ft_pct = table_drawers[10].text.strip().replace("%", "&#37;"),
            oreb = table_drawers[11].text.strip(),
            dreb = table_drawers[12].text.strip(),
            stl = table_drawers[16].text.strip(),
            to = table_drawers[15].text.strip(),
            blk = table_drawers[16].text.strip(),
            pfs = table_drawers[17].text.strip(),
            plus_minus = table_drawers[19].text.strip(),
            eff = table_drawers[20].text.strip()
            )