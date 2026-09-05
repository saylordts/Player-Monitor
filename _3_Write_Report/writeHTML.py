from _DClasses.report import Report
import subprocess

def writeHTML(mjml: str):
    html = subprocess.run(
        ["node", "_3_Write_Report/mjmlCompiler.js"],
        input=mjml,
        text=True,
        capture_output=True,
        check=True
    )
    return html.stdout