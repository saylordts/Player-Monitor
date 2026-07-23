from dataclasses import dataclass, field
from datetime import date
from DClasses.game import Game

@dataclass
class Player:
    URL: str
    games: list[Game] = field(default_factory=list)
    name: str = "N/A"
    last_game: date = date(1900, 1, 1)
    mjml: str = ""