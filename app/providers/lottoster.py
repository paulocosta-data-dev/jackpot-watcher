import re

import requests
from bs4 import BeautifulSoup

from app.models.jackpot import JackpotData
from app.providers.base import JackpotProvider
from app.utils.retry import (
    retry_with_backoff
)


class LottoStarProvider(JackpotProvider):

    URL = (
        "https://www.lottoster.com/"
        "pt/euromillions-por/jackpot/"
    )

    def fetch(self) -> JackpotData:

        response = retry_with_backoff(
            self._make_request
        )

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

        euromillions_block = (
            self._extract_euromillions_block(
                lines
            )
        )

        jackpot_amount = (
            self._extract_jackpot_amount(
                euromillions_block
            )
        )

        return JackpotData(
            amount=jackpot_amount,
            currency="EUR",
            draw_date="next_draw",
            draw_id=jackpot_amount,
            game="EuroMillions",
            source="lottoster-scraper"
        )

    def _make_request(self):

        # TEST ONLY
        # Uncomment to force retry failures
        #
        # raise Exception(
        #     "Forced retry failure."
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

        return response

    def _extract_euromillions_block(
        self,
        lines
    ):

        for index, line in enumerate(lines):

            if line == "Euromillones":

                block = lines[
                    index:index + 8
                ]

                return block

        raise ValueError(
            "Could not find "
            "Euromillones section."
        )

    def _extract_jackpot_amount(
        self,
        block
    ):

        for line in block:

            match = re.search(
                r"(\d{1,3}(?:\.\d{3})+)\€",
                line
            )

            if match:

                jackpot_raw = (
                    match.group(1)
                )

                return int(
                    jackpot_raw.replace(
                        ".",
                        ""
                    )
                )

        raise ValueError(
            "Could not extract "
            "EuroMillions jackpot."
        )