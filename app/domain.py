from app.data.ApplicationLog import ApplicationLog
from app.models.colors import Colors
import logging
import os
from app.services.Hue import Hue

from pydexcom import Dexcom
from rgbxy import Converter
from flask import current_app
logger = logging.getLogger()
converter = Converter()
dexcom = Dexcom(os.getenv("DEXCOM_USER"), os.getenv("DEXCOM_PASSWORD"))
hue = Hue()
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def update_lights_workflow():
    value = -1
    logger.debug("Update lights...")
    try:
        bg = dexcom.get_current_glucose_reading()
        if bg is not None:
            value = bg.value
        x, y = calculate_color(value)
        light_change_result = hue.change_color(x, y)
        logger.debug(light_change_result)
        # with current_app.app_context():
        #     if value > -1:
        #         app_log = ApplicationLog(
        #             value=value,
        #             hue_result=str(light_change_result),
        #             mg_dl=str(bg.mg_dl),
        #             mmol_l=str(bg.mmol_l),
        #             trend=str(bg.trend),
        #             trend_description=str(bg.trend_description),
        #             trend_arrow=str(bg.trend_arrow),
        #             reading_time=str(bg.time),
        #         )
        #     else:
        #         app_log = ApplicationLog(
        #             value=value
        #         )
        #     db.session.add(app_log)
        #     db.session.commit()
        return value
    except Exception:
        logger.exception(f"Could not change light colors")

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

    logger.info(f"Glucose Value is {glucose_value} and color is {color.name}")
    return converter.rgb_to_xy(*color.value)
