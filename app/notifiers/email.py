import smtplib
from email.message import EmailMessage

from app.models.jackpot import JackpotData


class EmailNotifier:

    def __init__(
        self,
        smtp_host,
        smtp_port,
        smtp_username,
        smtp_password,
        email_from,
        email_to
    ):

        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.email_to = email_to

    def send_jackpot_alert(
        self,
        jackpot: JackpotData,
        alert_type: str
    ):

        message = EmailMessage()

        formatted_amount = (
            f"€{jackpot.amount:,}"
        )

        if alert_type == "threshold":

            subject = (
                "🚨 EuroMillions Alert "
                "- Jackpot Above Threshold"
            )

            plain_text = (
                f"Current jackpot: "
                f"{formatted_amount}"
            )

            html = f"""
            <html>
                <body style="font-family: Arial;">

                    <h2>
                        🚨 EuroMillions Alert
                    </h2>

                    <p>
                        Threshold exceeded.
                    </p>

                    <p style="
                        font-size: 32px;
                        font-weight: bold;
                        text-decoration: underline;
                    ">
                        {formatted_amount}
                    </p>

                    <p>
                        <strong>Source:</strong>
                        {jackpot.source}
                    </p>

                </body>
            </html>
            """

        elif alert_type == "fallback":

            subject = (
                "⚠️ EuroMillions Warning "
                "- Fallback Mode Activated"
            )

            plain_text = (
                f"Fallback mode active.\n"
                f"Estimated jackpot: "
                f"{formatted_amount}"
            )

            html = f"""
            <html>
                <body style="font-family: Arial;">

                    <h2>
                        ⚠️ Fallback Mode Activated
                    </h2>

                    <p>
                        Primary provider failed.
                    </p>

                    <p style="
                        font-size: 32px;
                        font-weight: bold;
                        text-decoration: underline;
                    ">
                        {formatted_amount}
                    </p>

                    <p>
                        <strong>Source:</strong>
                        {jackpot.source}
                    </p>

                </body>
            </html>
            """

        elif alert_type == "heartbeat":

            subject = (
                "💓 Jackpot Watcher Heartbeat"
            )

            plain_text = (
                f"System operational.\n\n"
                f"Next jackpot estimate: "
                f"{formatted_amount}"
            )

            html = f"""
            <html>
                <body style="font-family: Arial;">

                    <h2>
                        💓 Jackpot Watcher Heartbeat
                    </h2>

                    <p>
                        System operational.
                    </p>

                    <p>
                        Next jackpot estimate:
                    </p>

                    <p style="
                        font-size: 32px;
                        font-weight: bold;
                        text-decoration: underline;
                    ">
                        {formatted_amount}
                    </p>

                    <p>
                        <strong>Provider:</strong>
                        {jackpot.source}
                    </p>

                </body>
            </html>
            """

        else:

            subject = (
                "EuroMillions Notification"
            )

            plain_text = (
                f"Jackpot amount: "
                f"{formatted_amount}"
            )

            html = f"""
            <html>
                <body>
                    <p>
                        {formatted_amount}
                    </p>
                </body>
            </html>
            """

        message["Subject"] = subject
        message["From"] = self.email_from
        message["To"] = self.email_to

        message.set_content(
            plain_text
        )

        message.add_alternative(
            html,
            subtype="html"
        )

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