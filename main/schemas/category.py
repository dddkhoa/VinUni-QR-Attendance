from marshmallow import fields

from main.schemas.base import BaseSchema, PaginationSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=BaseSchema.length_validator)
    user_id = fields.Integer(dump_only=True)


class CategoryListSchema(PaginationSchema):
    items = fields.Nested(CategorySchema(), many=True)
