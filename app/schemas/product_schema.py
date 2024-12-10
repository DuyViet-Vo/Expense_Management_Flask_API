from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    group_name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)
    stock = fields.Int(required=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
