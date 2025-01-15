from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.category_group_service import CategoryGroupService

category_group_bp = Blueprint("category-group", __name__, url_prefix="/api/category-group")

@category_group_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    result = CategoryGroupService.create_category_group(data)
    return jsonify(result), result["status"]


@category_group_bp.route("/get-all", methods=["GET"])
@jwt_required()
def get_all_category():
    result = CategoryGroupService.get_all_category_group()
    return jsonify(result), result["status"]


@category_group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_category(group_id: int):
    result = CategoryGroupService.delete_category_group(group_id)
    return jsonify(result), result["status"]
