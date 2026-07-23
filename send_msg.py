import smtplib
import ssl
from getpass import getpass

def send(msg, sender_email, debug=True):
    if debug:
        smtp_server = "localhost"
        port = 8025
        with smtplib.SMTP(smtp_server, port) as server:
            server.send_message(msg)

    else:
        smtp_server = "smtp.gmail.com"
        port = 465
        password = getpass("Type your password and press enter: ")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            smtp_server, port, context=context
        ) as server:
            server.login(sender_email, password)
            server.send_message(msg)
