import logging
import os
from sys import stdout
from app.daemon import interval_query
from dotenv import load_dotenv
from flask import Flask
import threading

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="templates")
    # app.config.from_pyfile(config_filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cgmlights.db"
    setup_logging()
    # from .data.ApplicationLog import db

    # db.init_app(app)
    register_blueprints(app)
    return app


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
