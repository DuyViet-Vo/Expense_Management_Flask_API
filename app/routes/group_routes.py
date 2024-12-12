from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.group_service import GroupService

group_bp = Blueprint("group", __name__, url_prefix="/api/groups")


@group_bp.route("", methods=["POST"])
@jwt_required()
def create_group():
    data = request.get_json()
    current_user = get_jwt_identity()
    result = GroupService.create_group(data, current_user)
    return jsonify(result), result["status"]


@group_bp.route("/<int:group_id>", methods=["PUT"])
@jwt_required()
def update_group(group_id):
    data = request.get_json()
    result = GroupService.update_group(group_id, data)
    return jsonify(result), result["status"]


@group_bp.route("/get-all", methods=["GET"])
@jwt_required()
def get_all_groups():
    result = GroupService.get_all_groups()
    return jsonify(result), result["status"]


@group_bp.route("/<int:group_id>", methods=["GET"])
@jwt_required()
def get_group(group_id):
    result = GroupService.get_group(group_id)
    return jsonify(result), result["status"]


@group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group(group_id):
    result = GroupService.delete_group(group_id)
    return jsonify(result), result["status"]


@group_bp.route("/delete-many", methods=["DELETE"])
@jwt_required()
def delete_many_group():
    data = request.get_json()
    result = GroupService.delete_many_group(data)
    return jsonify(result), result["status"]
