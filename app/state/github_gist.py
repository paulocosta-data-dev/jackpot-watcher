import json
from datetime import datetime, UTC

import requests

from app.config import Config


class GitHubGistStateManager:

    def __init__(self):

        if not Config.GIST_ID:
            raise ValueError(
                "Missing GIST_ID."
            )

        if not Config.GIST_TOKEN:
            raise ValueError(
                "Missing GIST_TOKEN."
            )

        self.base_url = (
            f"https://api.github.com/gists/"
            f"{Config.GIST_ID}"
        )

        self.headers = {
            "Authorization": (
                f"token {Config.GIST_TOKEN}"
            ),
            "Accept": "application/vnd.github+json"
        }

    def get_state(self) -> dict:

        response = requests.get(
            self.base_url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        gist_data = response.json()

        files = gist_data.get(
            "files",
            {}
        )

        state_file = files.get(
            "jackpot-state.json"
        )

        if not state_file:

            return self._default_state()

        content = state_file.get(
            "content",
            "{}"
        )

        try:

            return json.loads(content)

        except json.JSONDecodeError:

            return self._default_state()

    def update_alert_state(
        self,
        jackpot_amount,
        alert_type,
        source
    ):

        state = self.get_state()

        current_timestamp = (
            datetime.now(
                UTC
            ).isoformat()
        )

        updated_state = {
            "last_threshold_alert": (
                state.get(
                    "last_threshold_alert"
                )
            ),
            "last_fallback_alert": (
                state.get(
                    "last_fallback_alert"
                )
            ),
            "last_heartbeat_alert": (
                state.get(
                    "last_heartbeat_alert"
                )
            ),
            "last_seen_jackpot": (
                jackpot_amount
            ),
            "last_seen_source": (
                source
            ),
            "last_check_at": (
                current_timestamp
            )
        }

        if alert_type == "threshold":

            updated_state[
                "last_threshold_alert"
            ] = jackpot_amount

        elif alert_type == "fallback":

            updated_state[
                "last_fallback_alert"
            ] = current_timestamp

        elif alert_type == "heartbeat":

            updated_state[
                "last_heartbeat_alert"
            ] = current_timestamp

        payload = {
            "files": {
                "jackpot-state.json": {
                    "content": json.dumps(
                        updated_state,
                        indent=2
                    )
                }
            }
        }

        response = requests.patch(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

    def save_check_state(
        self,
        jackpot_amount,
        source
    ):

        state = self.get_state()

        current_timestamp = (
            datetime.now(
                UTC
            ).isoformat()
        )

        updated_state = {
            "last_threshold_alert": (
                state.get(
                    "last_threshold_alert"
                )
            ),
            "last_fallback_alert": (
                state.get(
                    "last_fallback_alert"
                )
            ),
            "last_heartbeat_alert": (
                state.get(
                    "last_heartbeat_alert"
                )
            ),
            "last_seen_jackpot": (
                jackpot_amount
            ),
            "last_seen_source": (
                source
            ),
            "last_check_at": (
                current_timestamp
            )
        }

        payload = {
            "files": {
                "jackpot-state.json": {
                    "content": json.dumps(
                        updated_state,
                        indent=2
                    )
                }
            }
        }

        response = requests.patch(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

    def _default_state(self):

        return {
            "last_threshold_alert": None,
            "last_fallback_alert": None,
            "last_heartbeat_alert": None,
            "last_seen_jackpot": None,
            "last_seen_source": None,
            "last_check_at": None
        }