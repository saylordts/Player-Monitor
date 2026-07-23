from report import Report
import subprocess

def writeHTML(report: Report):
    header = """<mjml>
  <mj-body>"""
    footer = """
  </mj-body>
</mjml>"""
    mjml = header
    for player in report.players:
        mjml = mjml+player.mjml
    mjml = mjml+footer
    html = subprocess.run(
        ["node", "mjmlCompiler.js"],
        input=mjml,
        text=True,
        capture_output=True,
        check=True
    )
    report.html = html.stdout
    return report