import os
from tqdm import tqdm
from _2_Run_Scrapers.PlayerScrapeError import PlayerScrapeError
from _DClasses.report import Report
import _2_Run_Scrapers.flashscoreScraper as fs
import _2_Run_Scrapers.proballersScraper as pb


def scraperCommander(report: Report):
    print("    1. Finding games...")
    report = fs.findDates(report)
    report = pb.findDates(report)
    print("    1. Finding games... DONE")
    
    for playerIndex, player in enumerate(report.players):
        report.players[playerIndex] = player.chooseDates()

    print("    2. Scraping games...")
    report = runScrapers(report)
    print("    2. Scraping games... DONE")

    return report


def runScrapers(report: Report):
    in_github_actions = os.getenv("GITHUB_ACTIONS") == "true"

    total_games = sum(len(player.use_games) for player in report.players)
    successful_count = 0; error_count = 0

    if in_github_actions:
        print("        • Scraping games - all servers...")
        progress = None
    else:
        progress = tqdm(
        total=total_games,
        desc="• Scraping games - all servers",
        unit="game",
        bar_format="        {desc}: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    )

    for playerIndex, player in enumerate(report.players):
        for use_game in player.use_games:
            if "flashscore" in use_game.link:
                try:
                    game = fs.scrapeOneGame(use_game.link, report.players[playerIndex])
                    if game:
                        report.players[playerIndex].games.append(game)
                        successful_count += 1
                except PlayerScrapeError as e:
                    report.errors.append(str(e))
                    error_count += 1
            elif "proballers" in use_game.link:
                try:
                    game = pb.scrapeOneGame(use_game.link,report.players[playerIndex])
                    if game:
                        report.players[playerIndex].games.append(game)
                        successful_count += 1
                except PlayerScrapeError as e:
                    report.errors.append(str(e))
                    error_count += 1
            if progress:
                progress.update(1)
                progress.set_postfix(
                    successful=successful_count,
                    errors=error_count
                )

        if player.games:
            report.players[playerIndex].team = player.games[-1].player_team

    if in_github_actions:
        print(f"        • Scraping games - all servers... DONE ({successful_count}/{total_games} successful)")
    return report