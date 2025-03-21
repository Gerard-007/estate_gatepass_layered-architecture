# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.auth_controller import auth_view
from controllers.gate_pass_controller import gate_pass_view
from helpers.config import Config
from helpers.db_connect import initialize_db


app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

initialize_db()

from helpers import custom_exceptions

app.register_blueprint(auth_view, url_prefix="/api/auth")
app.register_blueprint(gate_pass_view, url_prefix="/api/gate_pass")

if __name__ == "__main__":
    app.run(debug=True)
