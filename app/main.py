from datetime import datetime, UTC

from app.config import Config
from app.logger import setup_logger
from app.notifiers.email import EmailNotifier
from app.providers.fallback import (
    FallbackJackpotProvider
)
from app.rules.threshold_rule import ThresholdRule
from app.state.github_gist import (
    GitHubGistStateManager
)

logger = setup_logger()


def main():

    provider = (
        FallbackJackpotProvider()
    )

    jackpot = provider.fetch()

    logger.info(
        f"Jackpot amount: "
        f"€{jackpot.amount:,}"
    )

    logger.info(
        f"Provider source: "
        f"{jackpot.source}"
    )

    current_weekday = (
        datetime.now(
            UTC
        ).weekday()
    )

    logger.info(
        f"Current weekday: "
        f"{current_weekday}"
    )

    is_heartbeat_day = (
        current_weekday == 6
    )

    logger.info(
        f"Heartbeat day: "
        f"{is_heartbeat_day}"
    )

    if is_heartbeat_day:

        logger.info(
            "Running heartbeat flow."
        )

        notifier = EmailNotifier(
            smtp_host=Config.SMTP_HOST,
            smtp_port=Config.SMTP_PORT,
            smtp_username=Config.SMTP_USERNAME,
            smtp_password=Config.SMTP_PASSWORD,
            email_from=Config.EMAIL_FROM,
            email_to=Config.EMAIL_TO
        )

        notifier.send_jackpot_alert(
            jackpot=jackpot,
            alert_type="heartbeat"
        )

        state_manager = (
            GitHubGistStateManager()
        )

        state_manager.update_alert_state(
            jackpot_amount=jackpot.amount,
            alert_type="heartbeat",
            source=jackpot.source
        )

        logger.info(
            "Heartbeat sent."
        )

        return

    rule = ThresholdRule(
        threshold=Config.JACKPOT_THRESHOLD
    )

    threshold_exceeded = rule.evaluate(
        jackpot
    )

    fallback_mode = (
        jackpot.source ==
        "fallback-estimation"
    )

    state_manager = (
        GitHubGistStateManager()
    )

    state = state_manager.get_state()

    last_threshold_alert = state.get(
        "last_threshold_alert"
    )

    last_fallback_alert = state.get(
        "last_fallback_alert"
    )

    logger.info(
        f"Last threshold alert: "
        f"{last_threshold_alert}"
    )

    logger.info(
        f"Last fallback alert: "
        f"{last_fallback_alert}"
    )

    logger.info(
        f"Last seen jackpot: "
        f"{state.get('last_seen_jackpot')}"
    )

    logger.info(
        f"Last check at: "
        f"{state.get('last_check_at')}"
    )

    threshold_already_alerted = (
        str(last_threshold_alert) ==
        str(jackpot.amount)
    )

    fallback_already_alerted = (
        fallback_mode
        and last_fallback_alert
        is not None
    )

    logger.info(
        f"Threshold already alerted: "
        f"{threshold_already_alerted}"
    )

    logger.info(
        f"Fallback already alerted: "
        f"{fallback_already_alerted}"
    )

    if threshold_exceeded:

        should_alert = (
            not threshold_already_alerted
        )

        alert_type = "threshold"

    elif fallback_mode:

        should_alert = (
            not fallback_already_alerted
        )

        alert_type = "fallback"

    else:

        should_alert = False

        alert_type = None

    logger.info(
        f"Should alert: "
        f"{should_alert}"
    )

    logger.info(
        f"Alert type: "
        f"{alert_type}"
    )

    if should_alert:

        notifier = EmailNotifier(
            smtp_host=Config.SMTP_HOST,
            smtp_port=Config.SMTP_PORT,
            smtp_username=Config.SMTP_USERNAME,
            smtp_password=Config.SMTP_PASSWORD,
            email_from=Config.EMAIL_FROM,
            email_to=Config.EMAIL_TO
        )

        notifier.send_jackpot_alert(
            jackpot=jackpot,
            alert_type=alert_type
        )

        state_manager.update_alert_state(
            jackpot_amount=jackpot.amount,
            alert_type=alert_type,
            source=jackpot.source
        )

        logger.info(
            "Alert sent."
        )

    else:

        state_manager.save_check_state(
            jackpot_amount=jackpot.amount,
            source=jackpot.source
        )

        logger.info(
            "Check state saved."
        )


if __name__ == "__main__":
    main()