from player import Player
from game import Game
from report import Report

def writeMJML(report: Report):
    header = """
    <mj-wrapper background-color="#f0f0f0">
      <mj-section padding-bottom="0px">
        <mj-column width="90%" background-color="#ffffff" border-radius="8px" padding="20px">
          <mj-text font-size="24px" font-weight="bold" color="#333333" padding="20px">"""
    before_games = """</mj-text>
        </mj-column>
      </mj-section>
      <mj-section padding-top="5px">
        <mj-column border-radius="8px" background-color="#ffffff" width="80%" padding="0px">"""
    footer = """
        </mj-column>
      </mj-section>
    </mj-wrapper>"""

    for player in report.players:
        player.mjml = header+f"{player.name}"+before_games
        for game in player.games:
            player.mjml = player.mjml+f"""
          <mj-accordion icon-width="0px" border="none">
            <mj-accordion-element>
              <mj-accordion-title>
                <mj-raw>
                  <span style="display: block; width: 100%;">
                    <span style="display: inline-block; width: 70%; vertical-align: middle;">
                      <b style="font-size: 16px; color: #111111; display: block; margin-bottom: 4px;">
                        {game.date} {game.versus_text}
                      </b>
                      <span style="font-size: 13px; color: #555555;">
                        {game.pts} PTS | {game.reb} REB ({game.oreb} OFF) | {game.ass} AST | {game.mins} MI
                      </span>
                    </span>
                    <span style="display: inline-block; width: 28%; text-align: right; vertical-align: middle;">
                      <span style="padding: 4px 8px; background-color: #e0e0e0; border-radius: 4px; white-space: nowrap; font-size: 14px; font-weight: bold;">
                        {game.win_loss} {game.score}
                      </span>
                    </span>
                  </span>
                </mj-raw>
              </mj-accordion-title>
              <mj-accordion-text padding-top="0px">
                <span style="display: block; font-size: 13px; color: #666666; font-weight: normal; letter-spacing: 1px;">2PT {game.twos} | 3PT {game.threes} | FG&#37; {game.fg_pct} | FT {game.fts} ({game.ft_pct})</span>
                <span style="font-size: 13px; color: #666666; font-weight: normal; letter-spacing: 1px;">{game.stl} STL | {game.blk} BLK | {game.to} TO | {game.pfs} PF | &#177; {game.plus_minus} | EFF {game.eff}</span>
              </mj-accordion-text>
            </mj-accordion-element>
          </mj-accordion>"""
        player.mjml = player.mjml+footer

    return report
        