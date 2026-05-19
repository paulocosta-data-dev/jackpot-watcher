from app.logger import setup_logger
from app.models.jackpot import JackpotData
from app.providers.euromillions import (
    EuroMillionsProvider
)
from app.providers.lottoster import (
    LottoStarProvider
)

logger = setup_logger()


class FallbackJackpotProvider:

    def fetch(self) -> JackpotData:

        try:

            logger.info(
                "Using LottoStar provider."
            )

            return LottoStarProvider().fetch()

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

            jackpot = (
                EuroMillionsProvider()
                .fetch()
            )

            jackpot.source = (
                "fallback-estimation"
            )

            jackpot.error_message = (
                str(error)
            )

            return jackpot