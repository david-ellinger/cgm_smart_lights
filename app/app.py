import logging
import os
import threading
import time
from enum import Enum
from sys import stdout

import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from pydexcom import Dexcom
from rgbxy import Converter

load_dotenv()

dexcom = Dexcom(os.getenv("DEXCOM_USER"), os.getenv("DEXCOM_PASSWORD"))
hue_bridge_ip = os.getenv("HUE_BRIDGE_IP")
hue_bridge_username = os.getenv("HUE_BRIDGE_USERNAME")
app = Flask(__name__, template_folder="templates")
converter = Converter()

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] - %(message)s")
consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

SECONDS_TO_SLEEP = 120


def update_lights_workflow():
    logger.info("Update lights...")
    bg = dexcom.get_current_glucose_reading()
    x, y = calculate_color(bg.value)
    light_change_result = change_color(x, y)
    logger.debug(light_change_result)


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
        title="Glucose Reading <> Light Transition",
        reading=f"Glucose Reading: {bg.value} {bg.trend_arrow} {bg.time}",
        light_color=f"({x},{y})",
        light_change=str(light_change_result),
    )


class Colors(Enum):
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    RED_YELLOW = (255, 193, 0)
    YELLOW = (255, 255, 0)
    YELLOW_GREEN = (214, 255, 0)
    GREEN = (0, 255, 0)
    PURPLE = (103, 78, 167)


def calculate_color(glucose_value):
    color = None
    if glucose_value <= 50:
        color = Colors.RED
    elif 50 < glucose_value <= 60:
        color = Colors.RED_YELLOW
    elif 60 < glucose_value <= 70:
        color = Colors.YELLOW
    elif 70 < glucose_value <= 80:
        color = Colors.YELLOW_GREEN
    elif 80 < glucose_value <= 110:
        color = Colors.BLUE
    elif 110 < glucose_value <= 130:
        color = Colors.YELLOW_GREEN
    elif 130 < glucose_value <= 150:
        color = Colors.YELLOW
    elif 150 < glucose_value <= 180:
        color = Colors.RED_YELLOW
    elif 180 < glucose_value:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
