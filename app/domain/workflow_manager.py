import logging
import os
from app.services.Hue import Hue
from app.domain.colors import Colors
from pydexcom import Dexcom
from rgbxy import Converter
logger = logging.getLogger()
converter = Converter()
dexcom = Dexcom(os.getenv("DEXCOM_USER"), os.getenv("DEXCOM_PASSWORD"))
hue = Hue()

def update_lights_workflow():
    value = -1
    try:
        bg = dexcom.get_current_glucose_reading()
        if bg is not None:
            value = bg.value
        x, y = calculate_color(value)
        light_change_result = hue.change_color(x, y)
        print(light_change_result)
        return value
    except Exception:
        logger.exception(f"Could not change light colors")
        print("Could not change light colors")

def clear_light():
    x,y = converter.rgb_to_xy(*Colors.WHITE.value)
    hue.change_color(x, y)
    print("Setting light to default light")

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
    elif 200 < glucose_value <= 250:
        color = Colors.RED_YELLOW
    elif 250 < glucose_value:
        color = Colors.RED
    else:
        color = Colors.PURPLE

    print(f"Glucose Value is {glucose_value} and color is {color.name}")
    return converter.rgb_to_xy(*color.value)
