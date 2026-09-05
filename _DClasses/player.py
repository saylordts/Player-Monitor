from dataclasses import dataclass, field
from datetime import date
from _DClasses.game import Game

@dataclass
class Player:
    links: dict[str] = field(default_factory=dict)
    games: list[Game] = field(default_factory=list)
    name: str = "N/A"
    team: str = "N/A"
    last_game: date = date(1900, 1, 1)
    mjml: str = ""