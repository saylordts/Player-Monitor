from dataclasses import dataclass
from datetime import date

@dataclass
class Game:
    date: str
    versus_text: str
    win_loss: str
    score: str
    pts: str
    reb: str
    ass: str
    mins: str
    twos: str
    threes: str
    fg_pct: str
    fts: str
    ft_pct: str
    oreb: str
    dreb: str
    stl: str
    to: str
    blk: str
    pfs: str
    plus_minus: str
    eff: str
    
    
