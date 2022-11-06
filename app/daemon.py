import time

from app.domain import update_lights_workflow
import logging

logger = logging.getLogger()
SECONDS_TO_SLEEP = 60

def interval_query():
    while True:
        update_lights_workflow()
        logger.info(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
        time.sleep(SECONDS_TO_SLEEP)

