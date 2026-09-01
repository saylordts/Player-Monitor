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
    
    
