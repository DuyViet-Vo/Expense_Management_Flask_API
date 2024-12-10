from marshmallow import Schema, fields


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    group_name = fields.Str(required=True)
    user_create = fields.Int()
    create_at = fields.DateTime()
    updated_at = fields.DateTime()


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
