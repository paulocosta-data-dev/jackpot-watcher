import time

import requests

from app.models.jackpot import JackpotData
from app.providers.base import JackpotProvider


class EuroMillionsProvider(JackpotProvider):

    BASE_URL = "https://euromillions.api.pedromealha.dev/draws"

    MAX_RETRIES = 3

    RETRY_DELAY_SECONDS = 5

    def fetch(self) -> JackpotData:

        for attempt in range(
            1,
            self.MAX_RETRIES + 1
        ):

            try:

                response = requests.get(
                    self.BASE_URL,
                    timeout=10
                )

                response.raise_for_status()

                data = response.json()

                if not data:
                    raise ValueError(
                        "No draw data returned."
                    )

                latest_draw = data[-1]

                jackpot_amount = (
                    latest_draw.get("prize")
                )

                if jackpot_amount is None:
                    raise ValueError(
                        "Prize amount missing."
                    )

                return JackpotData(
                    amount=int(
                        float(jackpot_amount)
                    ),
                    currency="EUR",
                    draw_date=latest_draw.get(
                        "date",
                        "unknown"
                    ),
                    draw_id=latest_draw.get(
                        "draw_id"
                    ),
                    game="EuroMillions",
                    source="pedromealha-api"
                )

            except requests.HTTPError as error:

                status_code = (
                    error.response.status_code
                )

                print(
                    f"\nHTTP Error: "
                    f"{status_code}"
                )

                if status_code == 429:

                    print(
                        "Rate limited. "
                        "Retrying..."
                    )

                    time.sleep(
                        self.RETRY_DELAY_SECONDS
                    )

                    continue

                raise

            except Exception:
                raise

        raise RuntimeError(
            "Max retries exceeded "
            "for EuroMillions API."
        )