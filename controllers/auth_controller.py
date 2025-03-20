import jwt
from flask import Blueprint, request, jsonify
from helpers.db_config import Config, auth_service
from helpers.utility import send_mail


auth_view = Blueprint('auth', __name__)


@auth_view.route("/register", methods=["POST"])
def register():
    try:
        response = auth_service.register_user(request.json)
        send_mail(
            subject="Verify Your Email",
            body=f"Click this link to verify your email: {response['link']}",
            from_email="gerardnwazk@gmail.com",
            to_email=[request.json["email"]]
        )
        return jsonify({"message": response["message"]}), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_view.route("/verify/<token>", methods=["POST"])
def verify(token):
    try:
        data = request.json
        tokens = auth_service.verify_user(token, data.get("password"))
        return jsonify(tokens), 200
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "Invalid token."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_view.route("/login", methods=["POST"])
def login():
    try:
        tokens = auth_service.login_user(request.json.get("email"), request.json.get("password"))
        return jsonify(tokens), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
