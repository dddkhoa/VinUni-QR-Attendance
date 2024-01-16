from main import app, db
from main.commons.decorators import (
    check_existing_category,
    check_owner,
    jwt_required,
    validate_input,
)
from main.commons.exceptions import CategoryAlreadyExists
from main.models.category import CategoryModel
from main.schemas.base import PaginationSchema
from main.schemas.category import CategoryListSchema, CategorySchema


@app.route("/categories", methods=["GET"])
@validate_input(PaginationSchema)
def get_category_list(data):
    pagination = CategoryModel.query.paginate(
        data["page"], data["per_page"], max_per_page=20, error_out=False
    )

    response = CategoryListSchema().dump(pagination)
    return response


@app.route("/categories", methods=["POST"])
@jwt_required
@validate_input(CategorySchema)
def post_category(user_id, data):
    if CategoryModel.query.filter_by(name=data["name"]).one_or_none():
        raise CategoryAlreadyExists()

    category = CategoryModel(name=data["name"], user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return {}


@app.route("/categories/<int:category_id>", methods=["GET"])
@check_existing_category
def get_category(category, **__):
    return CategorySchema().dump(category)


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
