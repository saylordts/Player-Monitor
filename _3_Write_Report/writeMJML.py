from datetime import date
from _DClasses.report import Report
from _DClasses.game import Game

def writeMJML(report: Report):
    mjml = header()

    for  player in report.players:
        mjml += playerHeader(player.name, player.team)

        if player.games:
            for game in player.games:
                mjml += singleGame(game)
        else:
            mjml += noGames(player.last_game)

    mjml += footer()

    return mjml


def header():
    todayDate = date.today().strftime("%B %d, %Y")

    return f"""
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all padding="0px" />
      <mj-class name="player-section" padding-left="5%" padding-right="1%" padding-bottom="5px" padding-top="5px"/>
      <mj-class name="player-column" background-color="#ffffff" border-radius="8px" padding="20px"/>
      <mj-class name="player-name" font-size="24px" font-weight="bold" color="#333333" padding="0px"/>
      <mj-class name="player-team" font-size="16px" font-weight="bold" color="#333333" padding="10px 0px 0px 20px"/>
      <mj-class name="game-section" padding-left="10%" padding-right="1%" padding-top="5px" padding-bottom="5px"/>
      <mj-class name="game-column" background-color="#ffffff" border-radius="8px" padding="10px 15px"/>
      <mj-class name="game-stats" color="#555555" font-size="12px" line-height="18px" align="left" padding="0px"/>
			      
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f0f0f0">
    <mj-section padding="10px">
      <mj-column>
        <mj-text align="center">
          Email Update {todayDate}
        </mj-text>
      </mj-column>
    </mj-section>
"""


def playerHeader(player_name: str, player_team: str):
    return f"""
    <mj-section mj-class="player-section">
      <mj-column mj-class="player-column">
        <mj-text mj-class="player-name">
          {player_name}
        </mj-text>
        <mj-text mj-class="player-team">
          {player_team}
        </mj-text>
      </mj-column>
    </mj-section>
"""


def singleGame(game: Game):
    return f"""
    <mj-section mj-class="game-section">
      <mj-column mj-class="game-column">
        <mj-text mj-class="game-stats">
          <div style="font-size:16px; line-height:22px; font-weight:bold; color:#000000; text-align:center; padding-bottom:5px;">
            <span style="white-space:nowrap;">{game.date.strftime("%b %d, %Y")} {game.versus_text}</span>
            <span style="white-space:nowrap; display:inline-block; margin-left:20px;">{game.win_loss} {game.score}</span>
          </div>
            {game.pts} PTS | {game.reb} REB ({game.oreb} / {game.dreb}) | {game.ast} AST | {game.mins} MIN<br/>
            FG {game.fgs} ({game.fg_pct}) | FT {game.fts} ({game.ft_pct}) <br/>
            2PT {game.twos} ({game.twos_pct}) | 3PT {game.threes} ({game.threes_pct}) <br/>
          	{game.stl} STL | {game.blk} BLK | {game.to} TO | {game.pfs} PF | &#177; {game.plus_minus} | EFF {game.eff}
        </mj-text>
      </mj-column>
    </mj-section>
"""


def noGames(last_game_date: str):
    return f"""
    <mj-section
      padding-left="10%"
      padding-right="1%"
      padding-top="5px"
      padding-bottom="5px"
    >
      <mj-column
        background-color="#ffffff"
        border-radius="8px"
        padding="10px"
      >
        <mj-text
          font-size="16px"
          font-weight="bold"
          align="center"
          padding="0px"
        >
          No Games Since {last_game_date.strftime("%b %d, %Y")}
        </mj-text>
      </mj-column>
    </mj-section>
"""


def footer():
    return """
  </mj-body>
</mjml>
"""