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
    x,y = calculate_color(bg.value)
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
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)

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
    if glucose_value <= 60:
        print(f"Glucose Value is {glucose_value} and color is Red")
        return converter.rgb_to_xy(255,0,0) # Red
    elif glucose_value > 60 and glucose_value <= 70:
        print(f"Glucose Value is {glucose_value} and color is Red->Yellow ")
        return converter.rgb_to_xy(246, 109, 0) # Red -> Yellow
    elif glucose_value > 70 and glucose_value <= 80:
        print(f"Glucose Value is {glucose_value} and color is Yellow ")
        return converter.rgb_to_xy(215, 167, 0) # Yellow
    elif glucose_value > 80 and glucose_value <= 90:
        print(f"Glucose Value is {glucose_value} and color is Yellow -> Green")
        return converter.rgb_to_xy(160, 214, 0) # Yellow -> Green
    elif glucose_value > 90 and glucose_value <= 130:
        print(f"Glucose Value is {glucose_value} and color is Green")
        return converter.rgb_to_xy(0, 255, 0) # Green
    elif glucose_value > 130 and glucose_value <= 140:
        print(f"Glucose Value is {glucose_value} and color is Green -> Yellow")
        return converter.rgb_to_xy(160, 214, 0) # Green -> Yellow
    elif glucose_value > 140 and glucose_value <= 150:
        print(f"Glucose Value is {glucose_value} and color is Yellow")
        return converter.rgb_to_xy(215, 167, 0) # Yellow
    elif glucose_value > 150 and glucose_value <= 160:
        print(f"Glucose Value is {glucose_value} and color is Yellow -> Red")
        return converter.rgb_to_xy(246, 109, 0) # Yellow -> Red
    else:
        print(f"Glucose Value is {glucose_value} and color is Red")
        return converter.rgb_to_xy(255,0,0) # Red


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
