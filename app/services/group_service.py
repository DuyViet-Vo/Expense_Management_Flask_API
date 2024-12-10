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
        print("+++++", user_create)
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
        groups = Group.query.all()
        return {"data": groups_schema.dump(groups), "status": 200}
