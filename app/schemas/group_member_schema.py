from marshmallow import Schema, fields


class GroupMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    account = fields.Int(required=True)
    group = fields.Int(required=True)
    create_at = fields.DateTime()


group_member_schema = GroupMemberSchema()
groups_member_schema = GroupMemberSchema(many=True)
