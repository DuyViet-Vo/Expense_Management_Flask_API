from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.product_service import ProductService

product_bp = Blueprint("product", __name__, url_prefix="/api/products")


@product_bp.route("/get-all", methods=["GET"])
@jwt_required()
def get_all_products():
    result = ProductService.get_all_products()
    return jsonify(result), result["status"]


@product_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    result = ProductService.get_product(product_id)
    return jsonify(result), result["status"]


@product_bp.route("", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()
    result = ProductService.create_product(data)
    return jsonify(result), result["status"]


@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    result = ProductService.update_product(product_id, data)
    return jsonify(result), result["status"]


@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    result = ProductService.delete_product(product_id)
    return jsonify(result), result["status"]
