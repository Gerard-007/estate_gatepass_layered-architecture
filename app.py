from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from controllers.auth_controller import auth_view
from controllers.gate_pass_controller import gate_pass_view
from helpers.db_config import Config, initialize_db

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

initialize_db()

app.register_blueprint(auth_view, url_prefix="/api/auth")
app.register_blueprint(gate_pass_view, url_prefix="/api/gate_pass")

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "details": str(error)}), 500

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    revoked_token = app.config["REVOKED_TOKENS_COLLECTION"].find_one({"jti": jti})
    return revoked_token is not None

if __name__ == "__main__":
    app.run(debug=True)