from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/api/users")


@user_bp.route("/resgister", methods=["POST"])
def register():
    data = request.get_json()
    result = UserService.register(data)
    return jsonify(result), result["status"]


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = UserService.login(data)
    return jsonify(result), result["status"]


@user_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    result = UserService.change_password(current_user, data)
    return jsonify(result), result["status"]
