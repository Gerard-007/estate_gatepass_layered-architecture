import jwt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt

from data.models.auth_model import RevokedToken
from helpers.db_connect import auth_service
from helpers.utility import send_mail



auth_view = Blueprint("auth", __name__)


@auth_view.route("/register", methods=["POST"])
def register():
    try:
        response = auth_service.register_user(request.json)
        send_mail(
            subject="Verify Your Email",
            body=f"Click this link to verify your email: {response['verification_link']}",
            from_email="gerardnwazk@gmail.com",
            to_email=[request.json["email"]]
        )
        return jsonify({"message": "Verification email sent."}), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_view.route("/verify/<token>", methods=["POST"])
def verify(token):
    try:
        data = request.json
        print(f"password: {data['password']}")
        tokens = auth_service.verify_user(token, data['password'])
        return jsonify(tokens), 200
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "Invalid token."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_view.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        tokens = auth_service.login_user(email, password)
        return jsonify(tokens), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@auth_view.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        RevokedToken(jti=jti).save()
        response = jsonify({"message": "Successfully logged out"})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Logout failed"}), 400
