import time

from app.logger import setup_logger

logger = setup_logger()


def retry_with_backoff(
    function,
    retries=3,
    delays=None
):

    if delays is None:

        delays = [2, 4, 8]

    last_error = None

    for attempt in range(retries):

        try:

            return function()

        except Exception as error:

            last_error = error

            if attempt < retries - 1:

                delay = delays[attempt]

                logger.warning(
                    f"Request failed. "
                    f"Retrying in {delay}s..."
                )

                time.sleep(delay)

            else:

                logger.error(
                    "All retries failed."
                )

    raise last_error