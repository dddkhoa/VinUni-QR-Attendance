from main import app, db
from main.commons.decorators import (
    check_existing_category,
    check_existing_item,
    check_owner,
    jwt_required,
    validate_input,
)
from main.commons.exceptions import ItemAlreadyExists
from main.models.item import ItemModel
from main.schemas.base import PaginationSchema
from main.schemas.item import ItemListSchema, ItemSchema, ItemUpdateSchema


@app.route("/categories/<int:category_id>/items", methods=["GET"])
@check_existing_category
@validate_input(PaginationSchema)
def get_item_list(category_id, data, **__):

    pagination = ItemModel.query.filter_by(category_id=category_id).paginate(
        data["page"], data["per_page"], max_per_page=20, error_out=False
    )

    response = ItemListSchema().dump(pagination)
    return response


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required
@validate_input(ItemSchema)
@check_existing_category
@check_owner
def post_item(category_id, data, **__):

    # Check if item name already exists
    if ItemModel.query.filter_by(name=data["name"]).one_or_none():
        raise ItemAlreadyExists()

    # Create new item and save to db
    item = ItemModel(
        name=data["name"], description=data["description"], category_id=category_id
    )
    db.session.add(item)
    db.session.commit()
    return {}


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
@check_existing_category
@check_existing_item
def get_item(item, **__):
    return ItemSchema().dump(item)


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required
@validate_input(ItemUpdateSchema)
@check_existing_category
@check_existing_item
@check_owner
def put_item(item, data, **__):

    # Check if item name already exists
    if ItemModel.query.filter_by(name=data["name"]).one_or_none():
        raise ItemAlreadyExists()

    item.query.filter_by(id=item.id).update(data)
    db.session.commit()
    return {}


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required
@check_existing_category
@check_existing_item
@check_owner
def delete_item(item, **__):
    db.session.delete(item)
    db.session.commit()
    return {}
