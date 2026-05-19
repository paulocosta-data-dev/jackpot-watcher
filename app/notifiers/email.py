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
                "EuroMillions jackpot alert\n\n"
                f"Current estimate: "
                f"{formatted_amount}\n\n"
                "Threshold exceeded.\n\n"
                f"Source: "
                f"{jackpot.source}"
            )

            html = f"""
            <html>
                <body style="
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #222;
                ">

                    <h2>
                        🚨 EuroMillions Jackpot Alert
                    </h2>

                    <p>
                        The estimated jackpot has
                        exceeded your configured
                        threshold.
                    </p>

                    <p>
                        Current estimated jackpot:
                    </p>

                    <p style="
                        font-size: 32px;
                        font-weight: bold;
                        text-decoration: underline;
                        color: #0b5394;
                    ">
                        {formatted_amount}
                    </p>

                    <p>
                        <strong>Game:</strong>
                        {jackpot.game}
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
                "Fallback mode activated\n\n"
                "Primary provider failed.\n"
                "Using backup estimation.\n\n"
                f"Estimated jackpot: "
                f"{formatted_amount}"
            )

            html = f"""
            <html>
                <body style="
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #222;
                ">

                    <h2>
                        ⚠️ Fallback Mode Activated
                    </h2>

                    <p>
                        The primary jackpot provider
                        failed.
                    </p>

                    <p>
                        A backup estimation model
                        is currently being used.
                    </p>

                    <p>
                        Current estimated jackpot:
                    </p>

                    <p style="
                        font-size: 32px;
                        font-weight: bold;
                        text-decoration: underline;
                        color: #b45f06;
                    ">
                        {formatted_amount}
                    </p>

                    <p>
                        <strong>Source:</strong>
                        {jackpot.source}
                    </p>

                    <p>
                        Estimated rollover increase:
                        +€15,000,000
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
                        Jackpot amount:
                        <strong>
                            {formatted_amount}
                        </strong>
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