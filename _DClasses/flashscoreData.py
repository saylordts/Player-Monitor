from dataclasses import dataclass
from datetime import date, datetime

from _DClasses.game import Game

@dataclass
class FlashscoreData:
    pts: str
    reb: str
    ast: str
    min: str
    fgMade: str
    fgAtt: str
    twosMade: str
    twosAtt: str
    threesMade: str
    threesAtt: str
    ftMade: str
    ftAtt: str
    plus_minus: str
    oreb: str
    dreb: str
    pfs: str
    stl: str
    to: str
    blk: str
    blka: str
    date: str
    versus_text: str
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
        fgMade = clean_stat(self.fgMade)
        fgAtt = clean_stat(self.fgAtt)
        twosMade = clean_stat(self.twosMade)
        twosAtt = clean_stat(self.twosAtt)
        threesMade = clean_stat(self.threesMade)
        threesAtt = clean_stat(self.threesAtt)
        ftMade = clean_stat(self.ftMade)
        ftAtt = clean_stat(self.ftAtt)
        plus_minus = clean_stat(self.plus_minus)
        oreb = clean_stat(self.oreb)
        dreb = clean_stat(self.dreb)
        pfs = clean_stat(self.pfs)
        stl = clean_stat(self.stl)
        to = clean_stat(self.to)
        blk = clean_stat(self.blk)
        blka = clean_stat(self.blka)

        date = datetime.strptime(self.date, "%d/%m/%Y").date()
        
        try: 
            fg_pct = round((int(fgMade) / int(fgAtt)) * 100, 1) if int(fgAtt) > 0 else 0.0
            fg_pct = f"{fg_pct}%"
        except ValueError:
            fg_pct = "-"

        try:
            ft_pct = round((int(ftMade) / int(ftAtt)) * 100, 1) if int(ftAtt) > 0 else 0.0
            ft_pct = f"{ft_pct}%"
        except ValueError:
            ft_pct = "-"

        scores = [int(x) for x in self.score.split("-")]
        if self.home:
            score = f"{scores[0]}-{scores[1]}"
            win_loss = "W" if scores[0] > scores[1] else "L"

            opp_team = self.versus_text.split("v")
            player_team = opp_team[0]
            versus_text = f"v {opp_team[1].strip()}" if len(self.versus_text.split("v")) > 1 else self.versus_text.strip()
        else:
            score = f"{scores[1]}-{scores[0]}"
            win_loss = "W" if scores[1] > scores[0] else "L"

            opp_team = self.versus_text.split("v")
            player_team = opp_team[1]
            versus_text = f"@ {opp_team[0].strip()}" if len(self.versus_text.split("v")) > 1 else self.versus_text.strip()

        return Game(
            date = date,
            versus_text = versus_text,
            win_loss = win_loss,
            score = score,
            pts = pts,
            reb = reb,
            ast = ast,
            mins = min,
            twos = f"{twosMade}-{twosAtt}",
            threes = f"{threesMade}-{threesAtt}",
            fg_pct = fg_pct,
            fts = f"{ftMade}-{ftAtt}",
            ft_pct = ft_pct,
            oreb = oreb,
            dreb = dreb,
            stl = stl,
            to = to,
            blk = blk,
            pfs = pfs,
            plus_minus = plus_minus,
            eff = "-",
            gameSource = "flashscore",
            player_team= player_team
        )
