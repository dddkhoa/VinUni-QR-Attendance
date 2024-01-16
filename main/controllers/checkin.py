import time

import requests

from main import app, config, db
from main.commons.decorators import (
    check_existing_category,
    check_owner,
    jwt_required,
    validate_input,
)
from main.commons.exceptions import CategoryAlreadyExists
from main.libs.utils import generate_random_attendance_key
from main.models.category import CategoryModel

# from main.schemas.base import PaginationSchema
from main.schemas.checkin import QRSchema


@app.route("/api/qr/generate", methods=["GET"])
@validate_input(QRSchema)
def get_checkin_qr(data):
    global attendance_secret_key
    while True:
        attendance_secret_key = generate_random_attendance_key()
        url = config.GOOGLE_QR_API.format(attendance_secret_key)
        response = requests.get(url).content
        yield response

        time.sleep(3)


@app.route("/categories", methods=["POST"])
@jwt_required
# @validate_input(CategorySchema)
def post_category(user_id, data):
    if CategoryModel.query.filter_by(name=data["name"]).one_or_none():
        raise CategoryAlreadyExists()

    category = CategoryModel(name=data["name"], user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return {}


# @app.route("/categories/<int:category_id>", methods=["GET"])
# @check_existing_category
# def get_category(category, **__):
#     return CategorySchema().dump(category)


@app.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required
@check_existing_category
@check_owner
def delete_category(category, **__):
    for item in category.items:
        db.session.delete(item)
    db.session.delete(category)
    db.session.commit()
    return {}
