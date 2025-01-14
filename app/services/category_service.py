from flask import request
from app.extensions import db
from app.models.category import Category


class CategoryService:
    @staticmethod
    def create_category(data):
        name = data.get("name")
        if not name:
            return {"message": "Missing required fields", "status": 400}

        if Category.query.filter_by(name=name).first():
            return {"message": "Category name already exists! Please choose another name.",
                    "status": 409}  # 409 Conflict

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def get_all_category():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination = Category.query.paginate(page=page, per_page=per_page, error_out=False)
        category_items = [category.to_dict() for category in pagination.items]
        return {
            "data": category_items,
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
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return {"message": "Category not found!", "status": 404}
        db.session.delete(category)
        db.session.commit()
        return {
            "message": "Category delete successfully", "status": 200
        }
