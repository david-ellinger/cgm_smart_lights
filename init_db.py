from app.app import db,ApplicationLog, app

with app.app_context():
    db.create_all()
