from dataclasses import dataclass
from datetime import date

@dataclass
class Game:
    date: date # datetime.strptime(unf_date, "%b %d, %Y").date()
    versus_text: str # @ ...
    win_loss: str # W
    score: str 
    pts: str
    reb: str
    oreb: str
    dreb: str
    ast: str
    mins: str
    fgs: str
    fg_pct: str
    fts: str
    ft_pct: str
    twos: str
    twos_pct: str
    threes: str
    threes_pct: str
    stl: str
    blk: str
    to: str
    pfs: str
    plus_minus: str
    eff: str
    player_team: str