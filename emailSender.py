from send_msg import send
from email.message import EmailMessage
from report import Report

def sendEmail(report: Report):
    sender_email = "thesaylorbot@gmail.com"
    receiver_email = "saylordts@gmail.com"

    msg = EmailMessage()
    msg["to"] = receiver_email
    msg["from"] = sender_email
    msg["subject"] = "Players Update"

    text = """\
HTML Not Working"""

    html = report.html

    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    send(msg, sender_email, False)