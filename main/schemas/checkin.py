from marshmallow import fields

from main.schemas.base import BaseSchema


class QRSchema(BaseSchema):
    course_id = fields.Integer(required=True)
    date = fields.String(required=True)
    # assignment_id = fields.Integer(required=True)
