from app.config import Config
from app.notifiers.email import EmailNotifier
from app.providers.fallback import (
    FallbackJackpotProvider
)
from app.rules.threshold_rule import ThresholdRule
from app.state.github_gist import (
    GitHubGistStateManager
)


def main():

    provider = (
        FallbackJackpotProvider()
    )

    jackpot = provider.fetch()

    print("\n=== NEXT JACKPOT ESTIMATE ===\n")
    print(f"Amount: €{jackpot.amount:,}")
    print(f"Source: {jackpot.source}")

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

    print("\n=== RULE RESULT ===\n")

    print(
        f"Threshold exceeded: "
        f"{threshold_exceeded}"
    )

    print(
        f"Fallback mode: "
        f"{fallback_mode}"
    )

    state_manager = (
        GitHubGistStateManager()
    )

    state = state_manager.get_state()

    last_alerted_jackpot = state.get(
        "last_alerted_jackpot"
    )

    current_jackpot = (
        jackpot.amount
    )

    already_alerted = (
        str(last_alerted_jackpot) ==
        str(current_jackpot)
    )

    print("\n=== STATE ===\n")

    print(
        f"Last alerted jackpot: "
        f"{last_alerted_jackpot}"
    )

    print(
        f"Last seen jackpot: "
        f"{state.get('last_seen_jackpot')}"
    )

    print(
        f"Last check at: "
        f"{state.get('last_check_at')}"
    )

    print(
        f"Already alerted: "
        f"{already_alerted}"
    )

    should_alert = (
        threshold_exceeded
        or fallback_mode
    )

    if threshold_exceeded:

        alert_type = "threshold"

    elif fallback_mode:

        alert_type = "fallback"

    else:

        alert_type = None

    print(
        f"Should alert: "
        f"{should_alert}"
    )

    print(
        f"Alert type: "
        f"{alert_type}"
    )

    if (
        should_alert
        and not already_alerted
    ):

        print("\n=== SENDING EMAIL ===\n")

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

        state_manager.update_state(
            jackpot_amount=jackpot.amount,
            alert_type=alert_type,
            source=jackpot.source
        )

        print(
            "\n=== STATE UPDATED ===\n"
        )

    else:

        state_manager.save_check_state(
            jackpot_amount=jackpot.amount,
            source=jackpot.source
        )

        print(
            "\n=== CHECK STATE SAVED ===\n"
        )

        print(
            "\n=== NO ALERT NEEDED ===\n"
        )


if __name__ == "__main__":
    main()