import json

import requests

from app.config import Config


class GitHubGistStateManager:

    def __init__(self):
        if not Config.GIST_ID:
            raise ValueError(
                "Missing GIST_ID environment variable."
            )

        if not Config.GITHUB_TOKEN:
            raise ValueError(
                "Missing GITHUB_TOKEN environment variable."
            )

        self.base_url = (
            f"https://api.github.com/gists/"
            f"{Config.GIST_ID}"
        )

        self.headers = {
            "Authorization": (
                f"token {Config.GITHUB_TOKEN}"
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

        files = gist_data.get("files", {})

        state_file = files.get("jackpot-state.json")

        if not state_file:
            return {
                "last_alerted_draw_id": None
            }

        content = state_file.get("content", "{}")

        return json.loads(content)

    def update_state(self, draw_id: int):
        payload = {
            "files": {
                "jackpot-state.json": {
                    "content": json.dumps(
                        {
                            "last_alerted_draw_id": draw_id
                        },
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