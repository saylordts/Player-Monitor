from dataclasses import dataclass, field
from _DClasses.player import Player

@dataclass
class Report:
    players: list[Player] = field(default_factory=list)
    html: str = ""
    def getPlayerByName(self, name: str) -> Player:
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f"Player with name '{name}' not found in the report.")
    def getPlayerIndexByName(self, name: str) -> int:
        for index, player in enumerate(self.players):
            if player.name == name:
                return index
        raise ValueError(f"Player with name '{name}' not found in the report.")
