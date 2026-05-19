from app.models.jackpot import JackpotData


class ThresholdRule:

    def __init__(self, threshold: int):
        self.threshold = threshold

    def evaluate(self, jackpot: JackpotData) -> bool:
        return jackpot.amount > self.threshold