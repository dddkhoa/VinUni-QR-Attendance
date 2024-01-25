from marshmallow import fields

from main.schemas.base import BaseSchema
from main.schemas.student import StudentSchema


class SectionSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    course_id = fields.Integer(required=True)
    students = fields.List(fields.Nested(StudentSchema()), required=True)


class SectionListSchema(BaseSchema):
    sections = fields.Nested(SectionSchema(), required=True)
