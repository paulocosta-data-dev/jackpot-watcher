import smtplib
from email.message import EmailMessage

from app.models.jackpot import JackpotData


class EmailNotifier:

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        email_from: str,
        email_to: str
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.email_to = email_to

    def send_jackpot_alert(
        self,
        jackpot: JackpotData
    ):
        subject = (
            f"EuroMillions Jackpot Alert "
            f"€{jackpot.amount:,}"
        )

        body = f"""
EuroMillions jackpot exceeded threshold.

Game: {jackpot.game}
Amount: €{jackpot.amount:,}
Draw Date: {jackpot.draw_date}
Source: {jackpot.source}
"""

        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = self.email_from
        message["To"] = self.email_to

        message.set_content(body)

        with smtplib.SMTP(
            self.smtp_host,
            self.smtp_port
        ) as server:

            server.starttls()

            server.login(
                self.smtp_username,
                self.smtp_password
            )

            server.send_message(message)