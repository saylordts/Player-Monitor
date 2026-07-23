from send_msg import send
from email.message import EmailMessage
from DClasses.report import Report
import os

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def sendEmail(report: Report):
    sender_email = SENDER_EMAIL
    receiver_email = RECEIVER_EMAIL

    msg = EmailMessage()
    msg["to"] = receiver_email
    msg["from"] = sender_email
    msg["subject"] = "Players Update"

    text = """
Player update available.

Please view this email in an HTML-supported email client.
"""

    html = report.html

    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    send(msg, sender_email, False)