from dataclasses import dataclass, field
from datetime import date
from _DClasses.game import Game


@dataclass
class Date_Link:
    date: date
    link: str

@dataclass
class Dates_Links:
    flashscore: list[Date_Link] = field(default_factory=list)
    proballers: list[Date_Link] = field(default_factory=list)

@dataclass
class Player:
    profileLinks: dict[str, str] = field(default_factory=dict)
    games: list[Game] = field(default_factory=list)
    found_games: Dates_Links = field(default_factory=Dates_Links)
    use_games: list[str] = field(default_factory=list)
    name: str = "N/A"
    team: str = "N/A"
    last_game: date = date(1900, 1, 1)
    mjml: str = ""
    def chooseDates(self):
        fs_games = [game for game in self.found_games.flashscore if game.date > self.last_game]
        pb_games = [game for game in self.found_games.proballers if game.date > self.last_game]

        kept_games = pb_games
        kept_dates = [game.date for game in kept_games]
        for fs_game in fs_games:
            if fs_game.date not in kept_dates:
                kept_games.append(fs_game)

        kept_games.sort(key=lambda x: x.date)
        self.use_games = kept_games

        return self
    def getProballersID(self):
        return self.profileLinks["proballers"].split("/")[-2]