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

def interval_query():
    while True:
        print("Sleeping for 30 seconds...")
        time.sleep(30)
        update_lights_workflow()

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
        light_change=str(light_change_result)
    )

def update_lights_workflow():
    bg = dexcom.get_current_glucose_reading()
    print(bg)
    x,y = calculate_color(bg.value)
    light_change_result = change_color(x,y)
    print(light_change_result)

def calculate_color(glucose_value):
    if glucose_value <= 75:
        return converter.rgb_to_xy(255,0,0) # Red
    elif glucose_value > 75 and glucose_value <= 95:
        return converter.rgb_to_xy(255, 255, 0) # Yellow
    elif glucose_value > 95 and glucose_value <= 130:
        return converter.rgb_to_xy(0, 255, 0) # Red
    elif glucose_value > 130 and glucose_value <= 175:
        return converter.rgb_to_xy(255, 255, 0) # Yellow
    elif glucose_value > 130 and glucose_value <= 175:
        return converter.rgb_to_xy(0, 255, 0) # Red
    else:
        return converter.rgb_to_xy(0, 0, 255) # Blue

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
    print(result.json())
    return result.json()


def rgb2xyb(r, g, b):
    r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b / 12.92

    X = r * 0.4124 + g * 0.3576 + b * 0.1805
    Y = r * 0.2126 + g * 0.7152 + b * 0.0722
    Z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return X / (X + Y + Z), Y / (X + Y + Z), int(Y * 254)





if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
