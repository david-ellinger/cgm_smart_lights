import logging
import os
from sys import stdout
import time
from app.daemon import interval_query
from app.domain import update_lights_workflow
from dotenv import load_dotenv
from flask import Flask
import threading

load_dotenv()
SECONDS_TO_SLEEP = 5


def create_app():
    app = Flask(__name__, template_folder="templates")
    # app.config.from_pyfile(config_filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cgmlights.db"
    setup_logging()
    # from .data.ApplicationLog import db

    # db.init_app(app)
    register_blueprints(app)
    return app

def interval_query_temp():
    logger = logging.getLogger(__name__)
    while True:
        try:
            update_lights_workflow()
        except Exception as e:
            breakpoint()
            logger.exception("Error calling update lights workflow...")
        logger.info(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
        time.sleep(SECONDS_TO_SLEEP)

thread = threading.Thread(name="interval_query", target=interval_query_temp)
thread.daemon = True
thread.start()

def setup_logging():
    # Setup Logging
    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.get("LOGLEVEL", "WARNING"))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s [%(levelname)s] - %(message)s"
    )
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


def register_blueprints(a):
    from app.endpoints import bp

    a.register_blueprint(bp)


# TODO: Evaluate whether to keep this
# @atexit.register
# def close_application():
#     color = Colors.WHITE
#     logger.info(f"Application is shutting down; Turning light {color.name}")

#     x,y = converter.rgb_to_xy(*color.value)
#     change_color(x, y)
