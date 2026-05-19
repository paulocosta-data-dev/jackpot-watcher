from app.logger import setup_logger
from app.providers.euromillions import (
    EuroMillionsProvider
)
from app.providers.lottoster import (
    LottoStarProvider
)

logger = setup_logger()


class FallbackJackpotProvider:

    def fetch(self):

        try:

            logger.info(
                "Using LottoStar provider."
            )

            provider = LottoStarProvider()

            return provider.fetch()

        except Exception as error:

            logger.warning(
                "LottoStar provider failed."
            )

            logger.warning(
                str(error)
            )

            logger.warning(
                "Using fallback provider."
            )

            provider = (
                EuroMillionsProvider()
            )

            jackpot = provider.fetch()

            estimated_amount = int(
                jackpot.amount + 15000000
            )

            jackpot.amount = (
                estimated_amount
            )

            jackpot.source = (
                "fallback-estimation"
            )

            return jackpot