from typing import Optional

from flask import make_response

from main.schemas.exceptions import ErrorSchema


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class _ErrorCode:
    BAD_REQUEST = 400000
    VALIDATION_ERROR = 400001
    EMAIL_ALREADY_EXISTS = 400002
    ITEM_ALREADY_EXIST = 400003
    CATEGORY_ALREADY_EXIST = 400004
    INVALID_EMAIL_OR_PASSWORD = 4000055
    INVALID_ACCESS_TOKEN = 400006
    MISSING_ALL_FIELDS = 400007
    UNAUTHORIZED = 401000
    LACKING_ACCESS_TOKEN = 401001
    EXPIRED_ACCESS_TOKEN = 401002
    FORBIDDEN = 403000
    FORBIDDEN_NOT_OWNER = 403001
    NOT_FOUND = 404000
    CATEGORY_NOT_FOUND = 404001
    ITEM_NOT_FOUND = 404002
    METHOD_NOT_ALLOWED = 405000
    INTERNAL_SERVER_ERROR = 500000


class _ErrorMessage:
    BAD_REQUEST = "Bad request."
    EMAIL_ALREADY_EXIST = "Email already exists"
    ITEM_ALREADY_EXIST = "Item already exists"
    CATEGORY_ALREADY_EXIST = "Category already exists"
    INVALID_EMAIL_OR_PASSWORD = "Invalid email or password"
    INVALID_ACCESS_TOKEN = "Invalid access token"
    MISSING_ALL_FIELDS = "Missing all fields"
    VALIDATION_ERROR = "Validation error."
    UNAUTHORIZED = "Unauthorized."
    LACKING_ACCESS_TOKEN = "Lacking access token in headers"
    EXPIRED_ACCESS_TOKEN = "JWT expired"
    FORBIDDEN = "Forbidden."
    FORBIDDEN_NOT_OWNER = "Only owner can modify a category or an item"
    NOT_FOUND = "Not found."
    CATEGORY_NOT_FOUND = "Category not found"
    ITEM_NOT_FOUND = "Item not found"
    METHOD_NOT_ALLOWED = "Method not allowed."
    INTERNAL_SERVER_ERROR = "Internal server error."


class BaseError(Exception):
    def __init__(
        self,
        *,
        error_message=None,
        error_data=None,
        status_code: Optional[int] = None,
        error_code: Optional[int] = None,
    ):
        """
        Customize the response exception

        :param error_message: <string> Message field in the response body
        :param status_code: <number> HTTP status code
        :param error_data: <dict> Json body data
        :param error_code: <number> error code
        """
        if error_message is not None:
            self.error_message = error_message

        if status_code is not None:
            self.status_code = status_code

        if error_code is not None:
            self.error_code = error_code

        self.error_data = error_data

    def to_response(self):
        response = ErrorSchema().jsonify(self)

        return make_response(response, self.status_code)


class BadRequest(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.BAD_REQUEST
    error_code = _ErrorCode.BAD_REQUEST


class ValidationError(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.VALIDATION_ERROR
    error_code = _ErrorCode.VALIDATION_ERROR


class Unauthorized(BaseError):
    status_code = StatusCode.UNAUTHORIZED
    error_message = _ErrorMessage.UNAUTHORIZED
    error_code = _ErrorCode.UNAUTHORIZED


class Forbidden(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.FORBIDDEN
    error_code = _ErrorCode.FORBIDDEN


class NotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.NOT_FOUND
    error_code = _ErrorCode.NOT_FOUND


class MethodNotAllowed(BaseError):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_message = _ErrorMessage.METHOD_NOT_ALLOWED
    error_code = _ErrorCode.METHOD_NOT_ALLOWED


class InternalServerError(BaseError):
    status_code = StatusCode.INTERNAL_SERVER_ERROR
    error_message = _ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = _ErrorCode.INTERNAL_SERVER_ERROR


class LackingAccessToken(BaseError):
    status_code = StatusCode.UNAUTHORIZED
    error_message = _ErrorMessage.LACKING_ACCESS_TOKEN
    error_code = _ErrorCode.LACKING_ACCESS_TOKEN


class ExpiredAccessToken(BaseError):
    status_code = StatusCode.UNAUTHORIZED
    error_message = _ErrorMessage.EXPIRED_ACCESS_TOKEN
    error_code = _ErrorCode.EXPIRED_ACCESS_TOKEN


class InvalidAccessToken(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.INVALID_ACCESS_TOKEN
    error_code = _ErrorCode.INVALID_ACCESS_TOKEN


class ForbiddenNotOwner(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.FORBIDDEN_NOT_OWNER
    error_code = _ErrorCode.FORBIDDEN_NOT_OWNER


class EmailAlreadyExists(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.EMAIL_ALREADY_EXIST
    error_code = _ErrorCode.EMAIL_ALREADY_EXISTS


class ItemAlreadyExists(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.ITEM_ALREADY_EXIST
    error_code = _ErrorCode.ITEM_ALREADY_EXIST


class CategoryAlreadyExists(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.CATEGORY_ALREADY_EXIST
    error_code = _ErrorCode.CATEGORY_ALREADY_EXIST


class InvalidEmailOrPassword(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.INVALID_EMAIL_OR_PASSWORD
    error_code = _ErrorCode.INVALID_EMAIL_OR_PASSWORD


class CategoryNotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.CATEGORY_NOT_FOUND
    error_code = _ErrorCode.CATEGORY_NOT_FOUND


class ItemNotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.ITEM_NOT_FOUND
    error_code = _ErrorCode.ITEM_NOT_FOUND
