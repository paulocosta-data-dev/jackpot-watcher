import logging
import sys


def setup_logger():

    logger = logging.getLogger(
        "jackpot-watcher"
    )

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        (
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        )
    )

    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(
        formatter
    )

    logger.addHandler(handler)

    return logger