from marshmallow import fields

from main.schemas.base import BaseSchema


class StudentSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    sortable_name = fields.String(required=True)
    avatar_url = fields.String(required=True)
    active = fields.Boolean(required=True)
    login_id = fields.String(required=True)


class StudentListSchema(BaseSchema):
    students = fields.List(fields.Nested(StudentSchema()), required=True)
