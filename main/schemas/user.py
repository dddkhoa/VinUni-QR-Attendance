from string import ascii_lowercase, ascii_uppercase, digits

from marshmallow import fields, validates

from main.commons.exceptions import ValidationError
from main.schemas.base import BaseSchema


class RegisterUserSchema(BaseSchema):
    email = fields.Email(required=True, validate=BaseSchema.length_validator)
    password = fields.String(required=True, validate=BaseSchema.length_validator)

    @validates("password")
    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError(
                error_message="Passwords must have at least 6 characters"
            )

        has_lower = False
        has_upper = False
        has_digit = False

        for char in password:
            if char in ascii_lowercase:
                has_lower = True
            elif char in ascii_uppercase:
                has_upper = True
            elif char in digits:
                has_digit = True

        if not (has_upper and has_lower and has_digit):
            raise ValidationError(
                error_message="Password must include at least one "
                "lowercase letter, one uppercase letter, one digit"
            )


class LoginUserSchema(BaseSchema):
    email = fields.Email(required=True, validate=BaseSchema.length_validator)
    password = fields.String(required=True, validate=BaseSchema.length_validator)
