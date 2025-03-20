from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from data.models.auth_model import User
from helpers.db_config import gate_pass_service


gate_pass_view = Blueprint('gate_pass', __name__)


@gate_pass_view.route("/generate_gate_pass", methods=["POST"])
@jwt_required()
def generate_gate_pass():
    current_user = User.objects(email=get_jwt_identity()).first()
    if not current_user or current_user.status not in ["Resident", "Admin"]:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        return jsonify(gate_pass_service.generate_gate_pass(current_user, request.json)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@gate_pass_view.route("/validate_gate_pass/<token_id>", methods=["GET"])
@jwt_required()
def validate_gate_pass(token_id):
    current_user = User.objects(email=get_jwt_identity()).first()
    if not current_user or current_user.status != "Security":
        return jsonify({"error": "Unauthorized"}), 403
    try:
        return jsonify(gate_pass_service.validate_gate_pass(token_id, current_user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@gate_pass_view.route("/generate_exit_gate_pass/<token_id>", methods=["POST"])
@jwt_required()
def generate_exit_gate_pass(token_id):
    current_user = User.objects(email=get_jwt_identity()).first()
    if not current_user or current_user.status not in ["Resident", "Admin"]:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        return jsonify(gate_pass_service.generate_exit_gate_pass(token_id, current_user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
