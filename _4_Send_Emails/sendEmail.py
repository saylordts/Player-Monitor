from _4_Send_Emails.send_msg import send_msg
from email.message import EmailMessage
from _DClasses.report import Report
import os
from dotenv import load_dotenv

load_dotenv()

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


    print(f"HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
    print(f"Full email size: {len(msg.as_bytes()) / 1024:.1f} KB")

    send_msg(msg, sender_email, False)

def sendFailureEmail(text: str):
    sender_email = SENDER_EMAIL
    receiver_email = RECEIVER_EMAIL

    msg = EmailMessage()
    msg["to"] = receiver_email
    msg["from"] = sender_email
    msg["subject"] = "Players Update Failure(s)"

    text = text

    msg.set_content(text)

    send_msg(msg, sender_email, False)