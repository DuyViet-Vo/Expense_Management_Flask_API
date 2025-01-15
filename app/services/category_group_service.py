from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app.extensions import db
from app.models.category_group import CategoryGroup
from app.models.category import Category
from sqlalchemy.orm import joinedload

class CategoryGroupService:
    @staticmethod
    def create_category_group(data: dict):
        category = data.get("category")
        group = data.get("group")

        # Kiểm tra nếu không có category hoặc group
        if category is None or group is None:
            return {
                "message": "Category and group are required.",
                "status": 400
            }
        # Kiểm tra xem category có tồn tại trong bảng category
        try:
            existing_category = db.session.query(Category).filter_by(id=category).one()
        except NoResultFound:
            return {
                "message": f"Category with ID {category} does not exist.",
                "status": 404
            }
            # Kiểm tra xem category và group có trùng lặp trong bảng category_group
        existing_category_group = (
            db.session.query(CategoryGroup)
            .filter_by(category=category, group=group)
            .first()
        )
        if existing_category_group:
            return {
                "message": "The category group already exists.",
                "status": 409
            }
        # Tạo mới category_group
        try:
            category_group = CategoryGroup(category=category, group=group)
            db.session.add(category_group)
            db.session.commit()
            return {
                "message": "Category group created successfully!",
                "data": category_group.to_dict(),
                "status": 200
            }
        except IntegrityError as e:
            db.session.rollback()
            return {
                "message": "Failed to create category group. Integrity error occurred.",
                "error": str(e),
                "status": 500
            }

    @staticmethod
    def get_all_category_group():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        group_id = request.args.get("group", type=int)  # Lấy tham số group từ query string

        # Tạo truy vấn cơ sở dữ liệu
        query = CategoryGroup.query
        if group_id is not None:
            query = query.filter_by(group=group_id)  # Lọc dữ liệu theo group

        # Phân trang dữ liệu
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        # Chuẩn bị dữ liệu với thông tin chi tiết của category
        category_group_items = [
            {
                **category_group.to_dict(),  # Thông tin từ CategoryGroup
                "category": {
                    "id": category_group.category_detail.id,
                    "name": category_group.category_detail.name
                } if category_group.category_detail else None  # Kiểm tra nếu có category_detail
            }
            for category_group in pagination.items
        ]

        return {
            "data": category_group_items,
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
    def delete_category_group(category_group_id: int):
        category_group = CategoryGroup.query.get(category_group_id)
        if not category_group:
            return {"message": "Category group not found!", "status": 404}
        db.session.delete(category_group)
        db.session.commit()
        return {"message": "Category group delete successfully", "status": 200}
