
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.category_service import CategoryService

category_bp = Blueprint("category", __name__, url_prefix="/api/category")

@category_bp.route("",methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    result = CategoryService.create_category(data)
    return jsonify(result), result["status"]

@category_bp.route("/get-all", methods=["GET"])
@jwt_required()
def get_all_category():
    result = CategoryService.get_all_category()
    return jsonify(result), result["status"]

@category_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_category(group_id):
    result = CategoryService.delete_category(group_id)
    return jsonify(result),result["status"]