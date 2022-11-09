from app.tasks import add_together
from flask import Blueprint, jsonify
bp = Blueprint('home', __name__, url_prefix='/')
from dotenv import load_dotenv
load_dotenv()

@bp.route("/")
def home():
    return "Hello"

@bp.route("/start",methods=["POST"])
def start():
    add_together.delay(34,11)
    add_together.wait()
    return "True"
    # Temporary solution
    # thread = threading.Thread(target=interval_query, daemon=True)
    # thread.start()
    # return jsonify({'thread_name': str(thread.name),
    #                 'started': True})


@bp.route("/health")
def health():
    return "Ok"
