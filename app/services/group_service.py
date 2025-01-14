from flask import request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_

from app.extensions import db
from app.models.group import Group
from app.models.user import User
from app.schemas.group_schema import groups_schema


class GroupService:
    @staticmethod
    def create_group(data, user_create):
        group_name = data.get("group_name")
        # Use the column attribute from the User model
        user = User.query.filter(User.username == user_create).first()
        if not user:
            return {"message": "User not found", "status": 404}
        if not group_name:
            return {"message": "Missing required fields", "status": 400}
        group = Group(group_name=group_name, user_create=user.id)
        db.session.add(group)
        db.session.commit()
        return {"message": "Group created successfully", "data": group.to_dict(), "status": 201}

    @staticmethod
    def update_group(group_id, data):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return {"message": "User not found", "status": 404}

        group = Group.query.get(group_id)
        if not group:
            return {"message": "Group not found", "status": 404}

        group_name = data.get("group_name")
        if not group_name:
            return {"message": "Group name is required", "status": 400}

        group_exists = Group.query.filter(
            and_(Group.group_name == group_name, Group.user_create == user.id, Group.id != group_id)
        ).first()
        if group_exists:
            return {"message": "Group name already exists, please change to another name", "status": 400}

        group.group_name = group_name
        db.session.commit()
        return {"message": "Group updated successfully", "data": group.to_dict(), "status": 200}

    @staticmethod
    def get_group(group_id):
        group = Group.query.get(group_id)
        if not group:
            return {"message": "Group not found", "status": 404}
        return {"data": group.to_dict(), "status": 200}

    @staticmethod
    def delete_group(group_id):
        group = Group.query.get(group_id)
        if not group:
            return {"message": "Group not found", "status": 404}

        db.session.delete(group)
        db.session.commit()

        return {"message": "Product deleted successfully", "status": 200}

    @staticmethod
    def get_all_groups():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination = Group.query.paginate(page=page, per_page=per_page, error_out=False)
        groups = pagination.items

        groups_data = [
            {
                "id": group.id,
                "group_name": group.group_name,
                "user_create": group.user_create,
                "create_at": group.create_at,
                "updated_at": group.updated_at,
                "user": {
                    "id": group.user.id,
                    "username": group.user.username,
                    "email": group.user.email,
                }
                if group.user
                else None,
            }
            for group in groups
        ]
        return {
            "data": groups_data,
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
    def delete_many_group(data: dict):
        try:
            group_ids = data.get("group_ids", [])
            print("++++", group_ids)
            if not group_ids or not isinstance(group_ids, list):
                return {"message": "List of invalid group ids!", "status": 400}
            Group.query.filter(Group.id.in_(group_ids)).delete()
            db.session.commit()
            return {"message": f"Deleted successfully {group_ids} group", "status": 200}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "status": 500}
