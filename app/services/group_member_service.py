from flask import request

from app.extensions import db
from app.models.group_member import GroupMember
from app.schemas.group_member_schema import groups_member_schema


class GroupMemberService:
    @staticmethod
    def create_group_member(data: dict):
        account = data.get("account")
        group = data.get("group")
        group_member = GroupMember(account=account, group=group)
        db.session.add(group_member)
        db.session.commit()
        return {"message": "Group member created successfully", "data": group_member.to_dict(), "status": 201}

    @staticmethod
    def get_group_member(id_group_member: int):
        group_member = GroupMember.query.get(id_group_member)
        if not group_member:
            return {"message": "Group member not found", "status": 404}
        return {"data": group_member.to_dict(), "status": 200}

    @staticmethod
    def delete_group_member(id_group_member: int):
        group_member = GroupMember.query.get(id_group_member)
        if not group_member:
            return {"message": "Group member not found", "status": 404}
        db.session.delete(group_member)
        db.session.commit()
        return {"message": "Group member deleted successfully", "status": 200}

    @staticmethod
    def get_all_group_member():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination = GroupMember.query.paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items

        return {
            "data": groups_member_schema.dump(products),
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
    def delete_many_group_member(data: dict):
        try:
            group_member_ids = data.get("group_member_ids", [])
            if not group_member_ids or not isinstance(group_member_ids, list):
                return {"message": "List of invalid group member ids!", "status": 400}
            GroupMember.query.filter(GroupMember.id.in_(group_member_ids)).delete()
            db.session.commit()
            return {"message": f"Deleted successfully {group_member_ids} group member"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}
