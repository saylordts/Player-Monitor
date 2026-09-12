from dataclasses import dataclass
from datetime import date, datetime

from _DClasses.game import Game

@dataclass
class ProballersData:
    pts: str
    reb: str
    ast: str
    min: str
    twos: str
    threes: str
    fg_pct: str
    fts: str
    ft_pct: str
    plus_minus: str
    oreb: str
    dreb: str
    pfs: str
    stl: str
    to: str
    blk: str
    eff: str
    date: date
    home_team: str
    away_team: str
    score: str
    home: bool

    def toGame(self):
        def clean_stat(stat):
            if stat is None or stat.strip() in ["", "-"]:
                return "0"
            return stat.strip()
        pts = clean_stat(self.pts)
        reb = clean_stat(self.reb)
        ast = clean_stat(self.ast)
        min = clean_stat(self.min)
        twos = clean_stat(self.twos)
        threes = clean_stat(self.threes)
        fg_pct = clean_stat(self.fg_pct)
        fts = clean_stat(self.fts)
        ft_pct = clean_stat(self.ft_pct)
        plus_minus = clean_stat(self.plus_minus)
        oreb = clean_stat(self.oreb)
        dreb = clean_stat(self.dreb)
        pfs = clean_stat(self.pfs)
        stl = clean_stat(self.stl)
        to = clean_stat(self.to)
        blk = clean_stat(self.blk)
        eff = clean_stat(self.eff)

        date = datetime.strptime(self.date, "%b %d, %Y").date()

        scores = [int(x) for x in self.score.split("-")]
        if self.home:
            score = f"{scores[0]}-{scores[1]}"
            win_loss = "W" if scores[0] > scores[1] else "L"

            versus_text = f"v {self.away_team}"
            player_team = self.home_team
        else:
            score = f"{scores[1]}-{scores[0]}"
            win_loss = "W" if scores[1] > scores[0] else "L"

            versus_text = f"@ {self.home_team}"
            player_team = self.away_team

        try:
            twosMade = twos.split("-")[0]
            twosAtt = twos.split("-")[1]
            twos_pct = round((int(twosMade) / int(twosAtt)) * 100, 1) if int(twosAtt) > 0 else 0.0
            twos_pct = f"{twos_pct}%"
        except ValueError:
            twos_pct = "-"

        try:
            threesMade = threes.split("-")[0]
            threesAtt = threes.split("-")[1]
            threes_pct = round((int(threesMade) / int(threesAtt)) * 100, 1) if int(threesAtt) > 0 else 0.0
            threes_pct = f"{threes_pct}%"
        except ValueError:
            threes_pct = "-"

        try:
            fgs = f"{int(twosMade) + int(threesMade)}-{int(twosAtt) + int(threesAtt)}"
        except (ValueError, NameError):
            fgs = "-"

        return Game(
            date = date,
            versus_text = versus_text,
            win_loss = win_loss,
            score = score,
            pts = pts,
            reb = reb,
            oreb = oreb,
            dreb = dreb,
            ast = ast,
            mins = min,
            fgs = fgs,
            fg_pct = fg_pct,
            fts = fts,
            ft_pct = ft_pct,
            twos = twos,
            twos_pct = twos_pct,
            threes = threes,
            threes_pct = threes_pct,
            stl = stl,
            blk = blk,
            to = to,
            pfs = pfs,
            plus_minus = plus_minus,
            eff = eff,
            player_team = player_team
        )
