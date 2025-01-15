from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
from flask_jwt_extended import jwt_required

transaction_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

@transaction_bp.route("/", methods=["GET"])
@jwt_required()
def list_transactions():
    transactions = TransactionService.get_all_transactions()
    return jsonify(transactions)

@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_transaction(transaction_id):
    transaction = TransactionService.get_transaction_by_id(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction.to_dict())

@transaction_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_transaction():
    data = request.get_json()
    try:
        new_transaction = TransactionService.create_transaction(data)
        return jsonify(new_transaction.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field {str(e)}"}), 400

@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_existing_transaction(transaction_id):
    data = request.get_json()
    transaction = TransactionService.update_transaction(transaction_id, data)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction.to_dict())

@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_existing_transaction(transaction_id):
    transaction = TransactionService.delete_transaction(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"message": "Transaction deleted successfully"})
