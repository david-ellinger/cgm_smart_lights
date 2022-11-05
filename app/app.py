import atexit
import logging
import os
import sqlite3
import threading
import time
from sys import stdout

import requests
from app.models.colors import Colors
from dotenv import load_dotenv
from flask import Flask, render_template
from pydexcom import Dexcom
from rgbxy import Converter
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()

dexcom = Dexcom(os.getenv("DEXCOM_USER"), os.getenv("DEXCOM_PASSWORD"))
hue_bridge_ip = os.getenv("HUE_BRIDGE_IP")
hue_bridge_username = os.getenv("HUE_BRIDGE_USERNAME")
app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cgmlights.db"
db.init_app(app)


class ApplicationLog(db.Model):
    # TODO: Move this
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    hue_result = db.Column(db.String)
    mg_dl = db.Column(db.String)
    mmol_l = db.Column(db.String)
    trend = db.Column(db.String)
    trend_description = db.Column(db.String)
    trend_arrow = db.Column(db.String)
    reading_time = db.Column(db.String)


converter = Converter()

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] - %(message)s")
consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

SECONDS_TO_SLEEP = 60


def update_lights_workflow():
    logger.debug("Update lights...")
    try:
        bg = dexcom.get_current_glucose_reading()
        if bg is None:
            value = -1
        else:
            value = bg.value
        x, y = calculate_color(value)
        light_change_result = change_color(x, y)
        logger.debug(light_change_result)
        with app.app_context():
            if value > -1:
                app_log = ApplicationLog(
                    value=value,
                    hue_result=str(light_change_result),
                    mg_dl=str(bg.mg_dl),
                    mmol_l=str(bg.mmol_l),
                    trend=str(bg.trend),
                    trend_description=str(bg.trend_description),
                    trend_arrow=str(bg.trend_arrow),
                    reading_time=str(bg.time),
                )
            else:
                app_log = ApplicationLog(
                    value=value
                )
            db.session.add(app_log)
            db.session.commit()
    except Exception:
        logger.exception(f"Could not change light colors")


def interval_query():
    while True:
        update_lights_workflow()
        logger.info(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
        time.sleep(SECONDS_TO_SLEEP)


thread = threading.Thread(name="interval_query", target=interval_query, daemon=True)
thread.start()


@app.route("/")
def home():
    bg = dexcom.get_current_glucose_reading()
    x, y = calculate_color(bg.value)
    light_change_result = change_color(x, y)
    return render_template(
        "home.html",
        title="Glucose Reading",
        reading=f"{bg.value} {bg.trend_arrow} {bg.time}",
        light_color=f"({x},{y})",
        light_change=str(light_change_result),
    )

@app.route("/readings")
def readings():
    readings = ApplicationLog.query.order_by(desc(ApplicationLog.reading_time)).paginate(page=1, per_page=50,error_out=False).items
    return render_template(
        "readings.html", readings=readings
    )

@app.route("/health")
def health():
    return


def calculate_color(glucose_value):
    color = None
    if glucose_value == -1:
        color = Colors.PURPLE
    elif glucose_value < 55:
        color = Colors.RED
    elif 55 <= glucose_value <= 69:
        color = Colors.RED_YELLOW
    elif 70 <= glucose_value <= 79:
        color = Colors.YELLOW
    elif 80 <= glucose_value <= 150:
        color = Colors.BLUE
    elif 150 < glucose_value <= 200:
        color = Colors.GREEN
    elif 200 < glucose_value < 250:
        color = Colors.RED_YELLOW
    elif 250 < glucose_value:
        color = Colors.RED
    else:
        color = Colors.PURPLE

    logger.info(f"Glucose Value is {glucose_value} and color is {color.name}")
    return converter.rgb_to_xy(*color.value)


def change_color(x, y):
    headers = {
        "Accept": "application/json",
    }
    light = 3
    data = '{"on":true,"xy":[%.4f,%.4f]}' % (x, y)
    result = requests.put(
        f"http://{hue_bridge_ip}/api/{hue_bridge_username}/lights/{light}/state",
        headers=headers,
        data=data,
    )
    return result.json()

@atexit.register
def close_application():
    color = Colors.WHITE
    logger.info(f"Application is shutting down; Turning light {color.name}")

    x,y = converter.rgb_to_xy(*color.value)
    change_color(x, y)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


