import os
from tqdm import tqdm
from _2_Run_Scrapers.PlayerScrapeError import PlayerScrapeError
from _DClasses.report import Report
import _2_Run_Scrapers.flashscoreScraper as fs
import _2_Run_Scrapers.proballersScraper as pb


def scraperCommander(report: Report):
    report = fs.findDates(report)
    report = pb.findDates(report)

    report = runScrapers(report)

    return report

def runScrapers(report: Report):
    in_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    if in_github_actions:
        print("        • Scraping games - all servers...")
        player_iterator = report.players
    else:
        player_iterator = tqdm(
        report.players,
        desc="• Scraping games - all servers",
        unit="player",
        bar_format="        {desc}: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}"
    )
        
    proballers_success = 0; proballers_count = 0; flashscore_success = 0; flashscore_count = 0

    for playerIndex, player in enumerate(player_iterator):
        fs_games = [game for game in player.found_games.flashscore if game.date > player.last_game]
        pb_games = [game for game in player.found_games.proballers if game.date > player.last_game]

        dates = [game.date for game in pb_games]
        for fs_game in fs_games:
            if fs_game.date not in dates:
                dates.append(fs_game.date)
        dates.sort()

        gamesScraped = 0
        while gamesScraped < 5:
            for date in dates:
                if date in [game.date for game in pb_games]:
                    link = getLinkFromDate(player, date, "proballers")
                    proballers_count += 1
                    try:
                        game = pb.scrapeOneGame(link, player)
                        if game:
                            report.players[playerIndex].games.append(game)
                            proballers_success += 1
                            report.players[playerIndex].team = game.player_team
                            gamesScraped += 1
                            continue
                    except PlayerScrapeError as e:
                        report.errors.append(str(e))
                if date in [game.date for game in fs_games]:
                    link = getLinkFromDate(player, date, "flashscore")
                    flashscore_count += 1
                    try:
                        game = fs.scrapeOneGame(link, player)
                        if game:
                            report.players[playerIndex].games.append(game)
                            flashscore_success += 1
                            report.players[playerIndex].team = game.player_team
                            gamesScraped += 1
                            continue
                    except PlayerScrapeError as e:
                        report.errors.append(str(e))
            break
        
        if not in_github_actions:
            player_iterator.set_postfix(
                proballers=f"{proballers_success}/{proballers_count}",
                flashscore=f"{flashscore_success}/{flashscore_count}"
        )
    return report

def getLinkFromDate(player, date, source):
    if source == "flashscore":
        for game in player.found_games.flashscore:
            if game.date == date:
                return game.link
    elif source == "proballers":
        for game in player.found_games.proballers:
            if game.date == date:
                return game.link
    return None