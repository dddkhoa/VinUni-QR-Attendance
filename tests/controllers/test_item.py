import pytest

from main import db
from main.libs.utils import generate_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def create_user(email="a@gmail.com", password="Abc123"):
    user = UserModel(email, password)
    db.session.add(user)
    db.session.commit()
    return user


def create_category(name="new_cate", user_id=1):
    category = CategoryModel(name=name, user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return category


def create_item(name="new_item", description="new_desc", category_id=1):
    item = ItemModel(name=name, description=description, category_id=category_id)
    db.session.add(item)
    db.session.commit()
    return item


class TestGetItem:
    def _set_up(self):
        self.user = create_user()
        self.category = create_category(user_id=self.user.id)
        self.item = create_item(category_id=self.category.id)

    @pytest.mark.parametrize("page, per_page", [(1, 20), (2, 20)])
    def test_successful_pagination_get_item_lists(self, client, page, per_page):
        self._set_up()

        data = {
            "page": page,
            "per_page": per_page,
        }

        response = client.get(
            f"/categories/{self.category.id}/items", query_string=data
        )
        assert response.status_code == 200

        response_data = response.json
        page = response_data["page"]
        numbers_of_items_displayed = len(response_data["items"])
        if page == 1:
            assert numbers_of_items_displayed == 1
        elif page == 2:
            assert numbers_of_items_displayed == 0

    # Item with item_id 1 belongs to category_id 1
    def test_successful_get_one_item(self, client):
        self._set_up()

        response = client.get(
            f"/categories/{self.category.id}" f"/items/{self.item.id}"
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "page, per_page",
        [
            (
                "a",
                "b",
            ),
            # Invalid type for query params (which should be integer)
            # =>  validation error (400)
            ("", ""),
            ("a", 2),
        ],
    )
    def test_invalid_query_type_get_item_lists(self, client, page, per_page):
        self._set_up()

        data = {
            "page": page,
            "per_page": per_page,
        }
        response = client.get(
            f"/categories/{self.category.id}/items", query_string=data
        )
        assert response.status_code == 400

    def test_invalid_query_page_number_item_lists(self, client):
        self._set_up()

        data = {"page": 3, "per_page": 20}
        response = client.get(
            f"/categories/{self.category.id}/items", query_string=data
        )
        assert response.status_code == 200
        assert response.json["items"] == []

    def test_query_page_over_20_item_lists(self, client):
        self._set_up()

        data = {"page": 1, "per_page": 100}
        response = client.get(
            f"/categories/{self.category.id}/items", query_string=data
        )
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "invalid_category_id, invalid_item_id", [(91, ""), ("a", 1), ("", "")]
    )
    def test_invalid_get_item(self, client, invalid_category_id, invalid_item_id):
        self._set_up()

        response = client.get(
            f"/categories/{invalid_category_id}/items/{invalid_item_id}"
        )
        assert response.status_code == 404


class TestPostItem:
    def _set_up(self):
        self.user = create_user()
        self.category = create_category(user_id=self.user.id)
        self.item = ItemModel(
            name="post_item",
            description="post_description",
            category_id=self.category.id,
        )

    # successful_authentication -> jwt_token of user_id 1
    # successful when create item in category_id 1 (belongs to user_id 1)
    def test_successful_post_item(
        self,
        client,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        post_response = client.post(
            f"/categories/{self.category.id}/items",
            json={"name": self.item.name, "description": self.item.description},
            headers=successful_authentication,
        )
        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "item_1_1", "description": "desc1"},  # Item name already exists
            {
                "name": "",
                "description": "sample_desc",
            },
            {},  # Missing required field (item name and description),
            {
                "name": "     item_1_1",
                "description": "demo",
            },  # duplicate name but with leading whitespace
        ],
    )
    def test_invalid_post_item(
        self,
        client,
        data,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        post_response = client.post(
            f"/categories/{self.category.id}/items",
            json=data,
            headers=successful_authentication,
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_post_item(self, client):
        self._set_up()

        post_response = client.post(
            f"/categories/{self.category.id}/items",
            json={"name": self.item.name, "description": self.item.description},
            headers=[("Authorization", "Bearer ")],
        )
        assert post_response.status_code == 401

    # successful_authentication -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_post_item(
        self,
        client,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        forbidden_category_id = 2
        post_response = client.post(
            f"/categories/{forbidden_category_id}/items",
            json={"name": self.item.name, "description": self.item.description},
            headers=successful_authentication,
        )
        assert post_response.status_code == 403

    def test_not_found_post_item(
        self,
        client,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        not_found_category_id = 32
        post_response = client.post(
            f"/categories/{not_found_category_id}/items",
            json={"name": self.item.name, "description": self.item.description},
            headers=successful_authentication,
        )
        assert post_response.status_code == 404


class TestPutItem:
    def _set_up(self):
        self.user = create_user()
        self.category = create_category(user_id=self.user.id)
        self.item = create_item(category_id=self.category.id)

    def test_successful_put_item(
        self,
        client,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        data = {"name": "updated__item", "description": "updated_description"}

        post_response = client.put(
            f"/categories/{self.category.id}" f"/items/{self.item.id}",
            json=data,
            headers=successful_authentication,
        )

        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "item_1_2", "description": "desc1"},
            {},
            {"random": "random"},
            {"name": "   item_1_2"},
        ],
    )
    def test_invalid_put_item(
        self,
        client,
        data,
    ):
        self._set_up()
        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        post_response = client.put(
            f"/categories/{self.category.id}" f"/items/{self.item.id}",
            json=data,
            headers=successful_authentication,
        )

        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_put_item(self, client):
        self._set_up()

        post_response = client.put(
            f"/categories/{self.category.id}" f"/items/{self.item.id}",
            json={"name": self.item.name, "description": self.item.description},
            headers=[("Authorization", "Bearer ")],
        )
        assert post_response.status_code == 401

    # successful_authentication -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_put_item(
        self,
        client,
    ):
        self._set_up()

        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        forbidden_category_id = 2
        forbidden_item_id = 2
        post_response = client.put(
            f"/categories/{forbidden_category_id}/items/{forbidden_item_id}",
            json={"name": "aaa"},
            headers=successful_authentication,
        )
        assert post_response.status_code == 403

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(32, 1), (1, 2), (1, 91)]
    )
    def test_not_found_put_item(
        self,
        client,
        not_found_item_id,
        not_found_category_id,
    ):
        self._set_up()
        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        put_response = client.put(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            json={"name": "AAA"},
            headers=successful_authentication,
        )
        assert put_response.status_code == 404


class TestDeleteItem:
    def _set_up(self):
        self.user = create_user()
        self.category = create_category(user_id=self.user.id)
        self.item = create_item(category_id=self.category.id)

    def test_successful_delete_item(
        self,
        client,
    ):
        self._set_up()
        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        delete_response = client.delete(
            f"/categories/{self.category.id}" f"/items/{self.item.id}",
            headers=successful_authentication,
        )

        assert delete_response.status_code == 200

    def test_unauthorized_delete_item(self, client):
        self._set_up()

        delete_response = client.delete(
            f"/categories/{self.category.id}" f"/items/{self.item.id}",
            headers="",
        )
        assert delete_response.status_code == 401

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(32, 1), (1, 91)]
    )
    def test_not_found_delete_item(
        self,
        client,
        not_found_item_id,
        not_found_category_id,
    ):
        self._set_up()
        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        delete_response = client.delete(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            headers=successful_authentication,
        )
        assert delete_response.status_code == 404

    # In database, category_id 2 belongs to user_id 2
    # While successful_authentication returns JWT token of user_id 1
    # So a Forbidden (403) error should be raised
    def test_not_owner_delete_item(self, client):
        self._set_up()
        successful_authentication = [
            ("Authorization", f"Bearer {generate_jwt_token(self.user.id)}")
        ]

        delete_category_id = 2
        delete_item_id = 2
        delete_response = client.delete(
            f"/categories/{delete_category_id}/items/{delete_item_id}",
            headers=successful_authentication,
        )
        assert delete_response.status_code == 403

    def test_invalid_access_token(self, client):
        self._set_up()

        invalid_access_token = [("Authorization", "Bearer abc")]
        response = client.post(
            f"/categories/{self.category.id}/items",
            json={"name": self.item.name, "description": self.item.description},
            headers=invalid_access_token,
        )
        assert response.status_code == 400
