from functools import wraps

from flask import request
from marshmallow import ValidationError as MarshmallowValidationError

from main.commons.exceptions import (
    BadRequest,
    LackingAccessToken,
    ValidationError,
)
from main.libs.utils import decode_jwt_token


def jwt_required(func):
    @wraps(func)
    def decorator(**kwargs):
        try:
            token = request.headers["Authorization"].split()[1]
        except Exception:
            raise LackingAccessToken()
        user_id = decode_jwt_token(token)
        return func(user_id=user_id, **kwargs)

    return decorator


def validate_input(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            try:
                data = schema().load(_get_request_data())

            except MarshmallowValidationError as error:
                raise ValidationError(error_data=error.messages)

            except Exception as e:
                raise BadRequest(error_message=str(e))

            return func(data=data, **kwargs)

        return wrapper

    return decorator


def _get_request_data():
    if request.method in ("POST", "PUT"):
        data = request.get_json()
    else:
        data = dict(request.args)

    return data
