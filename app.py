from flask import Flask
from flask_cors import CORS
from .db import db

from .controllers.alarm_controller import alarm_controller

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    app.register_blueprint(alarm_controller)

    CORS(app)

    db.init_app(app)
    db.create_all(app=app)

    return app