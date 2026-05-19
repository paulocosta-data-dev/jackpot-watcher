from app.providers.euromillions import (
    EuroMillionsProvider
)
from app.providers.lottoster import (
    LottoStarProvider
)


class FallbackJackpotProvider:

    def fetch(self):

        try:

            print(
                "\nUsing LottoStar provider..."
            )

            provider = LottoStarProvider()

            return provider.fetch()

        except Exception as error:

            print(
                "\nLottoStar failed:"
            )

            print(error)

            print(
                "\nFalling back to "
                "historical API..."
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