import re

import requests
from bs4 import BeautifulSoup

from app.models.jackpot import JackpotData
from app.providers.base import JackpotProvider


class LottoStarProvider(JackpotProvider):

    URL = (
        "https://www.lottostar.com/"
        "euromillions/results"
    )

    def fetch(self) -> JackpotData:

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

        page_text = soup.get_text(
            separator=" ",
            strip=True
        )

        jackpot_match = re.search(
            r"(\d{1,3}(?:\.\d{3})+)\€",
            page_text
        )

        if not jackpot_match:
            raise ValueError(
                "Could not find jackpot amount."
            )

        jackpot_raw = jackpot_match.group(1)

        jackpot_amount = int(
            jackpot_raw.replace(".", "")
        )

        return JackpotData(
            amount=jackpot_amount,
            currency="EUR",
            draw_date="next_draw",
            draw_id=0,
            game="EuroMillions",
            source="lottoster-scraper"
        )