from dataclasses import dataclass


@dataclass
class JackpotData:

    amount: int
    currency: str
    draw_date: str
    draw_id: int
    game: str
    source: str
    error_message: str = ""