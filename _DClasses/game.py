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
    player_team: str
    player_team_ID: str

    def getStats(self):
        pts = int(self.pts)
        fgm = int(self.fgs.split("-")[0])
        fga = int(self.fgs.split("-")[-1])
        ftm = int(self.fts.split("-")[0])
        fta = int(self.fts.split("-")[-1])
        orb = int(self.oreb)
        drb = int(self.dreb)
        stl = int(self.stl)
        ast = int(self.ast)
        blk = int(self.blk)
        pf = int(self.pfs)
        tov = int(self.to)
        GS = pts + 0.4*fgm - 0.7*fga - 0.4*(fta-ftm) + 0.7*orb + 0.3*drb + stl +0.7*ast + 0.7*blk - 0.4*pf - tov
        GS36 = str(round(GS/36,1))
        GS = str(round(GS))
        TS = pts / 2 / (fga + .44*fta) * 100
        TS = str(round(TS,1)) + "%"
        return GS, GS36, TS