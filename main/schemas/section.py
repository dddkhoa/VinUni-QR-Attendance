from marshmallow import fields

from main.schemas.base import BaseSchema
from main.schemas.student import StudentSchema


class SectionSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    course_id = fields.Integer(required=False)
    students = fields.List(fields.Nested(StudentSchema()))


class SectionListSchema(BaseSchema):
    course_name = fields.String(required=True)
    section_list = fields.List(fields.Nested(SectionSchema()), required=True)
