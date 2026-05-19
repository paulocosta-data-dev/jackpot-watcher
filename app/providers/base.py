from abc import ABC, abstractmethod

from app.models.jackpot import JackpotData


class JackpotProvider(ABC):

    @abstractmethod
    def fetch(self) -> JackpotData:
        pass