import time

from app.domain import update_lights_workflow
import logging

logger = logging.getLogger(__name__)
SECONDS_TO_SLEEP = 5


def interval_query():
    while True:
        try:
            update_lights_workflow()
        except:
            logger.exception()
        logger.info(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
        time.sleep(SECONDS_TO_SLEEP)
