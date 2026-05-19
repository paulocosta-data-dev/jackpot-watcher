import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    GIST_ID = os.getenv("GIST_ID")

    GIST_TOKEN = os.getenv(
        "GIST_TOKEN"
    )

    threshold_raw = os.getenv(
        "JACKPOT_THRESHOLD"
    )

    JACKPOT_THRESHOLD = int(
        threshold_raw
    ) if threshold_raw else 100000000

    SMTP_HOST = os.getenv(
        "SMTP_HOST"
    )

    SMTP_PORT = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME"
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD"
    )

    EMAIL_FROM = os.getenv(
        "EMAIL_FROM"
    )

    EMAIL_TO = os.getenv(
        "EMAIL_TO"
    )