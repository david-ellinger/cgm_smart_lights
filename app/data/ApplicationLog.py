import sqlite3
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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
