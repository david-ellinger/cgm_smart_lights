from enum import Enum
import os
import threading
import time
import requests
from flask import Flask, render_template
from pydexcom import Dexcom
from dotenv import load_dotenv
from rgbxy import Converter

load_dotenv()

dexcom = Dexcom(os.getenv("DEXCOM_USER"), os.getenv("DEXCOM_PASSWORD"))
hue_bridge_ip = os.getenv("HUE_BRIDGE_IP")
hue_bridge_username = os.getenv("HUE_BRIDGE_USERNAME")
app = Flask(__name__, template_folder="templates")
converter = Converter()

SECONDS_TO_SLEEP = 60

def update_lights_workflow():
    bg = dexcom.get_current_glucose_reading()
    x,y = calculate_color(95)
    light_change_result = change_color(x,y)
    print(light_change_result)

def interval_query():
    while True:
        update_lights_workflow()
        print(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
        time.sleep(SECONDS_TO_SLEEP)

thread = threading.Thread(name='interval_query', target=interval_query)
thread.setDaemon(True)
thread.start()

class Colors(Enum):
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    RED_YELLOW = (255,193,0)
    YELLOW = (255, 255, 0)
    YELLOW_GREEN = (214,255,0)
    GREEN = (0, 255, 0)
    PURPLE = (103, 78, 167)

@app.route("/")
def home():
    bg = dexcom.get_current_glucose_reading()
    x,y = calculate_color(bg.value)
    light_change_result = change_color(x,y)
    return render_template(
        "home.html",
        title="Glucose Reading <> Light Transition",
        reading=f"Glucose Reading: {bg.value} {bg.trend_arrow} {bg.time}",
        light_color=f"({x},{y})",
        light_change=str(light_change_result)
    )



def calculate_color(glucose_value):
    color = None
    if glucose_value <= 60:
        color = Colors.RED
    elif 60 < glucose_value <= 70:
        color = Colors.RED_YELLOW
    elif 70 < glucose_value <= 80:
        color = Colors.YELLOW
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

    print(f"Glucose Value is {glucose_value} and color is {color.name}")
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
