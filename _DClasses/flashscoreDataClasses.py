from dataclasses import dataclass
from datetime import datetime

from _DClasses.game import Game
from _Data.teams import getTeamInfo

@dataclass
class FlashscoreData:
    id: str
    name: str
    def getProfileLink(self):
        return f"https://www.flashscore.com/player/{self.name}/{self.id}/"


@dataclass
class FlashscoreGame:
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
    homeID: str
    awayID: str
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

        try:
            twos_pct = round((int(twosMade) / int(twosAtt)) * 100, 1) if int(twosAtt) > 0 else 0.0
            twos_pct = f"{twos_pct}%"
        except ValueError:
            twos_pct = "-"

        try:
            threes_pct = round((int(threesMade) / int(threesAtt)) * 100, 1) if int(threesAtt) > 0 else 0.0
            threes_pct = f"{threes_pct}%"
        except ValueError:
            threes_pct = "-"

        homeName = self.versus_text.split(" v ")[0]
        awayName = self.versus_text.split(" v ")[-1]

        [homeID, homeName, homeSubtext]= getTeamInfo("flashscore",self.homeID,homeName)
        [awayID, awayName, awaySubtext] = getTeamInfo("flashscore",self.awayID,awayName)

        scores = [int(x) for x in self.score.split("-")]
        if self.home:
            score = f"{scores[0]}-{scores[1]}"
            win_loss = "W" if scores[0] > scores[1] else "L"

            player_team_ID = homeID
            player_team_name = homeName
            versus_text = f"v {awayName}"
        else:
            score = f"{scores[1]}-{scores[0]}"
            win_loss = "W" if scores[1] > scores[0] else "L"

            player_team_ID = awayID
            player_team_name = awayName
            versus_text = f"@ {homeName}"

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
            fgs = f"{fgMade}-{fgAtt}",
            fg_pct = fg_pct,
            fts = f"{ftMade}-{ftAtt}",
            ft_pct = ft_pct,
            twos = f"{twosMade}-{twosAtt}",
            twos_pct = twos_pct,
            threes = f"{threesMade}-{threesAtt}",
            threes_pct = threes_pct,
            stl = stl,
            blk = blk,
            to = to,
            pfs = pfs,
            plus_minus = plus_minus,
            player_team=player_team_name,
            player_team_ID=player_team_ID
        )
