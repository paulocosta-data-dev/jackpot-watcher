from app.config import Config
from app.notifiers.email import EmailNotifier
from app.providers.lottoster import (
    LottoStarProvider
)
from app.rules.threshold_rule import ThresholdRule
from app.state.github_gist import (
    GitHubGistStateManager
)


def main():

    provider = LottoStarProvider()

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

    print("\n=== RULE RESULT ===\n")
    print(
        f"Threshold exceeded: "
        f"{threshold_exceeded}"
    )

    state_manager = (
        GitHubGistStateManager()
    )

    state = state_manager.get_state()

    last_alerted_draw_id = state.get(
        "last_alerted_draw_id"
    )

    current_draw_id = (
        f"{jackpot.amount}"
    )

    already_alerted = (
        str(last_alerted_draw_id) ==
        str(current_draw_id)
    )

    print("\n=== STATE ===\n")
    print(
        f"Last alerted draw id: "
        f"{last_alerted_draw_id}"
    )

    print(
        f"Already alerted: "
        f"{already_alerted}"
    )

    if (
        threshold_exceeded
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
            jackpot
        )

        state_manager.update_state(
            current_draw_id
        )

        print(
            "\n=== STATE UPDATED ===\n"
        )

    else:

        print(
            "\n=== NO ALERT NEEDED ===\n"
        )


if __name__ == "__main__":
    main()