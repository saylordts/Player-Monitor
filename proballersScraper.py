import requests
from bs4 import BeautifulSoup
from datetime import datetime
from DClasses.game import Game
from DClasses.report import Report

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

def proballersScraper(report: Report):
    for player in report.players:
        try:
          page = requests.get(player.URL, headers=headers, timeout=20)
          page.raise_for_status()
        except requests.RequestException as e:
          print(f"Failed to scrape {player.URL}: {e}")
          continue
        soup = BeautifulSoup(page.content, "html.parser")

        identity = soup.find("h1", class_="identity__name")

        if identity is None:
            raise Exception(
                f"Could not find player identity page: {player.URL}"
            )
        first_name = identity.find("span", class_="firstname")
        last_name = identity.find("span", class_="lastname")
        full_name = first_name.text + " " + last_name.text

        player.name = full_name
        
        last_five = soup.find(id="anchor-last5games")
        table_all = last_five.find(
            "table", class_="table"
        )
        table_body = table_all.tbody
        table_rows = table_body.find_all("tr")
        
        for table_row in table_rows:
            table_drawers = table_row.find_all("td")
            
            game_date = table_drawers[0].a.text.strip()

            game_date_form = datetime.strptime(game_date, "%b %d, %Y")
            cutoff_date_form = datetime.strptime(player.last_game, "%Y-%m-%d")
            
            if game_date_form > cutoff_date_form:
                player.games.append(
                    Game(
                        date = game_date,
                        versus_text = table_drawers[1].a.text.strip(),
                        win_loss = table_drawers[3].span.text.strip(),
                        score = table_drawers[4].a.text.strip(),
                        pts = table_drawers[5].text.strip(),
                        reb = table_drawers[6].text.strip(),
                        ass = table_drawers[7].text.strip(),
                        mins = table_drawers[8].text.strip(),
                        twos = table_drawers[9].text.strip(),
                        threes = table_drawers[10].text.strip(),
                        fg_pct = table_drawers[11].text.strip().replace("%", "&#37;"),
                        fts = table_drawers[12].text.strip(),
                        ft_pct = table_drawers[13].text.strip().replace("%", "&#37;"),
                        oreb = table_drawers[14].text.strip(),
                        dreb = table_drawers[15].text.strip(),
                        stl = table_drawers[18].text.strip(),
                        to = table_drawers[19].text.strip(),
                        blk = table_drawers[20].text.strip(),
                        pfs = table_drawers[21].text.strip(),
                        plus_minus = table_drawers[22].text.strip(),
                        eff = table_drawers[24].text.strip()
                        )
                    )
    return report


