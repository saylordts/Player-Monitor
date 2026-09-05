from datetime import date
from _DClasses.report import Report
from _DClasses.game import Game

def writeMJML(report: Report):
  mjml = header()
  for playerIndex, player in enumerate(report.players):
    mjml += playerHeader(player.name, player.team)
    for gameIndex, game in enumerate(player.games):
      if gameIndex == 0: 
         mjml += gameHeader()
      mjml += singleGame(game)
      if gameIndex < len(player.games) - 1:
        mjml += gameSpacer()
      elif gameIndex == len(player.games) - 1:
        mjml += gameFooter()
    if playerIndex < len(report.players) - 1:
      mjml += playerSpacer()
  mjml += footer()

  with open("__0_Testing/report.html", "w") as f:
      f.write(mjml)
            
  return mjml

def header():
  todayDate = date.today().strftime("%B %d, %Y")
  return f"""<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all padding="0px" />
      <mj-class name="game-top" background-color="#ffffff" border-radius="8px 8px 0px 0px" />
      <mj-class name="game-bottom" background-color="#ffffff" border-radius="0px 0px 8px 8px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f0f0f0">
    <mj-section padding="10px">
      <mj-column>
        <mj-text align="center">Email Update {todayDate} </mj-text>
      </mj-column>
    </mj-section>"""

def playerHeader(player_name: str, player_team: str):
  return f"""    <mj-wrapper padding-left="5%" padding-right="1%" padding-bottom="5px">
      <mj-section>
        <mj-column background-color="#ffffff" border-radius="8px">
          <mj-text font-size="24px" font-weight="bold" color="#333333" padding="20px 20px 0px 20px">{player_name}</mj-text>
          <mj-text font-size="16px" font-weight="bold" color="#333333" padding="10px 20px 20px 40px">{player_team}</mj-text>
        </mj-column>
      </mj-section>
    </mj-wrapper>"""

def gameHeader():
   return "    <mj-wrapper padding-left='10%' padding-right='1%'>"

def singleGame(game:Game):
   return f"""      <mj-section mj-class="game-top" padding-top="5px" padding-bottom="5px">
        <mj-group>
          <mj-column vertical-align="middle" width="75%">
            <mj-text font-size="16px" font-weight="bold" align="center">
              {game.date.strftime("%B %d, %Y")} {game.versus_text}
            </mj-text>
          </mj-column>
          <mj-column vertical-align="middle" width="25%">
            <mj-text font-size="16px" font-weight="bold" align="left">{game.win_loss} {game.score}</mj-text>
          </mj-column>
        </mj-group>
      </mj-section>
      <mj-section mj-class="game-bottom" padding-bottom="5px">
        <mj-column padding-left="15px">
          <mj-text color="#555555" padding-top="5px" font-size="13px" align="left">
            {game.pts} PTS | {game.reb} REB ({game.oreb} OFF) | {game.ast} AST | {game.mins} MIN
          </mj-text>
          <mj-text color="#555555" padding-top="5px" font-size="12px" align="left">
            2PT {game.twos} | 3PT {game.threes} | FG&#37; {game.fg_pct} | FT {game.fts} ({game.ft_pct})
          </mj-text>
          <mj-text color="#555555" padding-top="5px" font-size="12px" align="left">
            {game.stl} STL | {game.blk} BLK | {game.to} TO | {game.pfs} PF | &#177; {game.plus_minus} | EFF {game.eff}
          </mj-text>
        </mj-column>
      </mj-section>"""

def gameFooter():
   return "    </mj-wrapper>"

def gameSpacer():
   return "      <mj-section><mj-column><mj-spacer height='5px'></mj-spacer></mj-column></mj-section>"

def playerSpacer():
   return "      <mj-section><mj-column><mj-spacer height='10px'></mj-spacer></mj-column></mj-section>"

def footer():
   return """  </mj-body>
</mjml>"""