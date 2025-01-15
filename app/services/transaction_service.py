from app.models.transactions import Transaction
from app.extensions import db
from flask import request


class TransactionService:
    @staticmethod
    def get_all_transactions():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        group_id = request.args.get("group", type=int)
        user_id = request.args.get("account", type=int)

        query = Transaction.query
        if user_id:
            query = query.filter(Transaction.account == user_id)
        if group_id:
            query = query.filter(Transaction.group == group_id)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        transaction_item = [transaction.to_dict() for transaction in pagination]

        return  {
            "data": transaction_item,
            "status": 200,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }

    @staticmethod
    def get_transaction_by_id(transaction_id):
        return Transaction.query.get(transaction_id)

    @staticmethod
    def create_transaction(data):
        new_transaction = Transaction(
            group=data["group"],
            account=data["account"],
            category=data["category"],
            amount=data["amount"],
            description=data["description"],
        )
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction

    @staticmethod
    def update_transaction(transaction_id, data):
        transaction = TransactionService.get_transaction_by_id(transaction_id)
        if not transaction:
            return None

        transaction.group = data.get("group", transaction.group)
        transaction.account = data.get("account", transaction.account)
        transaction.category = data.get("category", transaction.category)
        transaction.amount = data.get("amount", transaction.amount)
        transaction.description = data.get("description", transaction.description)
        db.session.commit()
        return transaction

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = TransactionService.get_transaction_by_id(transaction_id)
        if not transaction:
            return None

        db.session.delete(transaction)
        db.session.commit()
        return transaction
