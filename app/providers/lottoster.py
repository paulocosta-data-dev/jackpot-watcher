import re

import requests
from bs4 import BeautifulSoup

from app.models.jackpot import JackpotData
from app.providers.base import JackpotProvider


class LottoStarProvider(JackpotProvider):

    URL = (
        "https://www.lottoster.com/"
        "pt/euromillions-por/jackpot/"
    )

    def fetch(self) -> JackpotData:

        # TEST ONLY
        # Uncomment to force fallback mode

        # raise Exception(
        #    "Forced LottoStar failure for testing."
        # )

        response = requests.get(
            self.URL,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        lines = [
            line.strip()
            for line in soup.get_text(
                separator="\n"
            ).splitlines()
            if line.strip()
        ]

        jackpot_amount = None

        for index, line in enumerate(lines):

            if line == "Euromillones":

                next_lines = lines[
                    index:index + 5
                ]

                for candidate in next_lines:

                    match = re.search(
                        r"(\d{1,3}(?:\.\d{3})+)\€",
                        candidate
                    )

                    if match:

                        jackpot_raw = (
                            match.group(1)
                        )

                        jackpot_amount = int(
                            jackpot_raw.replace(
                                ".",
                                ""
                            )
                        )

                        break

            if jackpot_amount:
                break

        if not jackpot_amount:

            raise ValueError(
                "Could not find "
                "EuroMillions jackpot."
            )

        return JackpotData(
            amount=jackpot_amount,
            currency="EUR",
            draw_date="next_draw",
            draw_id=jackpot_amount,
            game="EuroMillions",
            source="lottoster-scraper"
        )