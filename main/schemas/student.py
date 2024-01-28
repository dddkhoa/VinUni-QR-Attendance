from marshmallow import fields

from main.schemas.base import BaseSchema


class StudentSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    sortable_name = fields.String(required=True)
    avatar_url = fields.String(required=True)
    active = fields.Boolean(required=True)
    login_id = fields.String(required=True)  # email


class StudentListSchema(BaseSchema):
    students = fields.List(fields.Nested(StudentSchema()), required=True)


class StudentRecord(BaseSchema):
    id = fields.String(required=True)
    date = fields.Date(required=True)
    status = fields.String(required=True)


class StudentRecordList(BaseSchema):
    # student_id = fields.Integer(required=True)
    attendanceRecords = fields.List(fields.Nested(StudentRecord()), required=True)
