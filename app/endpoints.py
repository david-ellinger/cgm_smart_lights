from flask import current_app, Blueprint, render_template, abort
from .domain import update_lights_workflow
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route("/")
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

@bp.route("/reading",methods=["POST"])
def reading():
    value = update_lights_workflow()
    return str(value) if value > -1 else abort(500)

@bp.route("/readings")
def readings():
    # readings = ApplicationLog.query.order_by(desc(ApplicationLog.reading_time)).paginate(page=1, per_page=50,error_out=False).items
    # return render_template(
    #     "readings.html", readings=readings
    # )
    return "Readings"

@bp.route("/health")
def health():
    return "Ok"
