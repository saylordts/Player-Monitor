from dataclasses import dataclass, field
from game import Game

@dataclass
class Player:
    URL: str
    games: list[Game] = field(default_factory=list)
    name: str = "N/A"
    last_game: str = "1900-01-01"
    mjml: str = ""