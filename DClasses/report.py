from dataclasses import dataclass, field
from DClasses.player import Player

@dataclass
class Report:
    players: list[Player] = field(default_factory=list)
    html: str = ""
