import atexit
import logging
import os
import sqlite3
import threading
import time
from sys import stdout

import requests
from app.domain import update_lights_workflow
from dotenv import load_dotenv
from flask import Flask, render_template

from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cgmlights.db"
db.init_app(app)





# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] - %(message)s")
consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)






# def interval_query():
#     while True:
#         update_lights_workflow()
#         logger.info(f"Sleeping for {SECONDS_TO_SLEEP} seconds...")
#         time.sleep(SECONDS_TO_SLEEP)


# thread = threading.Thread(name="interval_query", target=interval_query, daemon=True)
# thread.start()


@app.route("/")
def home():
    return "Hello"
    # bg = dexcom.get_current_glucose_reading()
    # x, y = calculate_color(bg.value)
    # light_change_result = change_color(x, y)
    # return render_template(
    #     "home.html",
    #     title="Glucose Reading",
    #     reading=f"{bg.value} {bg.trend_arrow} {bg.time}",
    #     light_color=f"({x},{y})",
    #     light_change=str(light_change_result),
    # )

@app.route("/reading")
def reading():
    print(update_lights_workflow())
    return True

@app.route("/readings")
def readings():
    # readings = ApplicationLog.query.order_by(desc(ApplicationLog.reading_time)).paginate(page=1, per_page=50,error_out=False).items
    # return render_template(
    #     "readings.html", readings=readings
    # )
    return "Readings"

@app.route("/health")
def health():
    return







#TODO: Evaluate whether to keep this
# @atexit.register
# def close_application():
#     color = Colors.WHITE
#     logger.info(f"Application is shutting down; Turning light {color.name}")

#     x,y = converter.rgb_to_xy(*color.value)
#     change_color(x, y)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


