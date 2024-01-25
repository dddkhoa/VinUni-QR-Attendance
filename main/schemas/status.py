from marshmallow import fields

from main.schemas.base import BaseSchema


class StatusSchema(BaseSchema):
    # id = fields.Integer(required=True)
    class_date = fields.Date(required=True)
    section_id = fields.Integer(required=True)
    student_id = fields.Integer(required=True)
    attendance = fields.String(required=True)
    course_id = fields.Integer(required=True)
    instructor_id = fields.Integer(required=True)


class StatusUpdateSchema(BaseSchema):
    student_id = fields.Integer(required=True)
    section_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    class_date = fields.Date(required=True)
    attendance = fields.String(required=False)


class StatusListSchema(BaseSchema):
    statuses = fields.List(fields.Nested(StatusSchema()), required=True)
