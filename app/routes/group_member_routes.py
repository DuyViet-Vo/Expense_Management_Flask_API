from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.group_member_service import GroupMemberService

group_member_bp = Blueprint("group-member", __name__, url_prefix="/api/group-member")


@group_member_bp.route("", methods=["POST"])
@jwt_required()
def create_group_member():
    data = request.get_json()
    result = GroupMemberService.create_group_member(data)
    return jsonify(result), result["status"]


@group_member_bp.route("/get-all", methods=["GET"])
@jwt_required()
def get_all_groups_member():
    result = GroupMemberService.get_all_group_member()
    return jsonify(result), result["status"]


@group_member_bp.route("/<int:group_member_id>", methods=["GET"])
@jwt_required()
def get_group_member(group_member_id):
    result = GroupMemberService.get_group_member(group_member_id)
    return jsonify(result), result["status"]


@group_member_bp.route("/<int:group_member_id>", methods=["DELETE"])
@jwt_required()
def delete_group_member(group_member_id):
    result = GroupMemberService.delete_group_member(group_member_id)
    return jsonify(result), result["status"]


@group_member_bp.route("/delete-many", methods=["DELETE"])
@jwt_required()
def delete_many_group():
    data = request.get_json()
    result = GroupMemberService.delete_many_group_member(data)
    return jsonify(result), result["status"]
