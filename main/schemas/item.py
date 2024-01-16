from marshmallow import ValidationError, fields, validates_schema

from main.schemas.base import BaseSchema, PaginationSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=BaseSchema.length_validator)
    description = fields.String(required=True, validate=BaseSchema.length_validator)
    category_id = fields.Integer(dump_only=True)


class ItemUpdateSchema(BaseSchema):
    name = fields.String(validate=BaseSchema.length_validator)
    description = fields.String(validate=BaseSchema.length_validator)

    @validates_schema
    def validate_not_all_fields_missing(self, data, **__):
        if (data.get("name") is None) and (data.get("description") is None):
            raise ValidationError(message="All fields are missing")


class ItemListSchema(PaginationSchema):
    items = fields.Nested(ItemSchema(), many=True)
