from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, pre_load, validate


class BaseSchema(Schema):
    length_validator = validate.And(
        validate.Length(min=1, error="Fields cannot be blank"),
        validate.Length(max=256, error="Maximum length of fields is 256"),
    )

    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    @pre_load
    def strip_whitespace(self, data, **__):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data


class PaginationSchema(BaseSchema):
    # If user input per_page > 20 -> raise Error
    per_page_range_validator = validate.Range(1, 20)

    per_page = fields.Integer(load_default=20, validate=per_page_range_validator)
    page = fields.Integer(load_default=1)
    total = fields.Integer(dump_only=True)
