from marshmallow import fields

from main.schemas.base import BaseSchema


class StatusSchema(BaseSchema):
    id = fields.Integer(required=False)
    class_date = fields.Date(required=True)
    section_id = fields.Integer(required=True)
    student_id = fields.Integer(required=True)
    status = fields.String(required=True)
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


class StudentStatusDateSchema(BaseSchema):
    name = fields.String(required=True)
    email = fields.String(required=True)  # similar to login_id in StudentSchema
    section = fields.Integer(required=True)  # section_id
    imageUrl = fields.String(required=True)
    status = fields.String(required=True)
    id = fields.Integer(required=True)  # status_id


class StudentStatusDateListSchema(BaseSchema):
    date = fields.Date(required=True)
    students = fields.List(fields.Nested(StudentStatusDateSchema()), required=True)
