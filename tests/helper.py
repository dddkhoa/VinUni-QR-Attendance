from main import db
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def setup_db():
    setup_user()
    setup_category()
    setup_item()


def setup_user():
    users = [
        UserModel(email="a@gmail.com", password="Abc123"),
        UserModel(email="b@gmail.com", password="Def456"),
        UserModel(email="c@gmail.com", password="Xyz789"),
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()


def setup_category():
    categories_1 = [CategoryModel(name=f"cate_1_{i}", user_id=1) for i in range(1, 11)]
    categories_2 = [CategoryModel(name=f"cate_2_{i}", user_id=2) for i in range(1, 11)]
    categories_3 = [CategoryModel(name=f"cate_3_{i}", user_id=3) for i in range(1, 11)]

    for cate1, cate2, cate3 in zip(categories_1, categories_2, categories_3):
        db.session.add(cate1)
        db.session.add(cate2)
        db.session.add(cate3)
    db.session.commit()


def setup_item():
    items_1 = [
        ItemModel(name=f"item_1_{i}", description=f"desc_1_{i}", category_id=1)
        for i in range(1, 31)
    ]

    items_2 = [
        ItemModel(name=f"item_2_{i}", description=f"desc_2_{i}", category_id=2)
        for i in range(1, 31)
    ]

    items_3 = [
        ItemModel(name=f"item_3_{i}", description=f"desc_3_{i}", category_id=3)
        for i in range(1, 31)
    ]

    for item1, item2, item3 in zip(items_1, items_2, items_3):
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)

    db.session.commit()
