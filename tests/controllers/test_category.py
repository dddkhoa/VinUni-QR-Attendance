import pytest


class TestCategory:

    # Successful Test Cases

    # In catalog_test, category table have 30 categories,
    # max categories per page should be 20, so the number of
    # categories on page 1 should be 20, page 2 should be 10

    @pytest.mark.parametrize("page, per_page", [(1, 20), (2, 20)])
    def test_successful_pagination_get_category_lists(self, client, page, per_page):
        data = {
            "page": page,
            "per_page": per_page,
        }
        response = client.get("/categories", query_string=data)
        assert response.status_code == 200

        response_data = response.json
        page = response_data["page"]
        numbers_of_categories_displayed = len(response_data["items"])
        if page == 1:
            assert numbers_of_categories_displayed == 20
        elif page == 2:
            assert numbers_of_categories_displayed == 10

    def test_successful_get_category(self, client):
        category_id = 1
        response = client.get(f"/categories/{category_id}")
        assert response.status_code == 200

    def test_successful_post_category(self, client, successful_authentication):
        data = {"name": "New Category"}
        post_response = client.post(
            "/categories", json=data, headers=successful_authentication
        )
        assert post_response.status_code == 200

    def test_successful_delete_all_items_in_category(
        self, client, successful_authentication
    ):
        category_id = 1
        delete_response = client.delete(
            f"/categories/{category_id}", headers=successful_authentication
        )
        assert delete_response.status_code == 200

        get_category_failed_response = client.get(f"/categories/{category_id}")
        get_item_list_failed_response = client.get(
            "/categories/1/items", query_string=dict(page=1, per_page=20)
        )

        assert get_category_failed_response.status_code == 404
        assert get_item_list_failed_response.status_code == 404

    # -----------------------FAILED TEST CASE-------------

    @pytest.mark.parametrize(
        "page, per_page",
        [
            (
                "a",
                "b",
            ),  # Invalid type for query params (which should be integer)
            # => validation error (400)
            ("", ""),
            ("a", 2),
        ],
    )
    def test_invalid_query_type_get_category_lists(self, client, page, per_page):
        data = {
            "page": page,
            "per_page": per_page,
        }
        response = client.get("/categories", query_string=data)
        assert response.status_code == 400

    # In catalog_test, category table have 30 categories,
    # max categories per page should be 20, so the number of
    # categories on page 1 should be 20, page 2 should be 10,
    # and page 3 should have no category, thus lead to
    # empty items
    def test_invalid_query_page_number_category_lists(self, client):
        data = {"page": 3, "per_page": 20}
        response = client.get("/categories", query_string=data)
        assert response.status_code == 200
        assert response.json["items"] == []

    def test_query_page_over_20_category_lists(self, client):
        data = {"page": 1, "per_page": 100}
        response = client.get("/categories", query_string=data)
        assert response.status_code == 400

    # There are only 30 categories whose ids labeled from 1->30,
    # so no category with id 31 or "a" -> 404
    @pytest.mark.parametrize("invalid_category_id", [31, "a", ""])
    def test_invalid_get_category(self, client, invalid_category_id):
        response = client.get(f"/categories/{invalid_category_id}")
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "cate_1_1"},  # Category name already exists
            {"name": ""},  # Missing required field (category name)
        ],
    )
    def test_invalid_post_category(self, client, successful_authentication, data):

        post_response = client.post(
            "/categories", json=data, headers=successful_authentication
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_post_category(self, client):
        data = {"name": "New Category"}
        post_response = client.post(
            "/categories", json=data, headers=[("Authorization", "")]
        )
        assert post_response.status_code == 401

    @pytest.mark.parametrize("invalid_category_id", [31, "a", ""])
    def test_invalid_delete_category(
        self, client, successful_authentication, invalid_category_id
    ):
        delete_response = client.delete(
            f"/categories/{invalid_category_id}", headers=successful_authentication
        )
        assert delete_response.status_code == 404

    # In database, category_id 11 belongs to user_id 2
    # While successful_authentication returns JWT token of user_id 1
    # So a Forbidden (403) error should be raised
    def test_not_owner_delete_category(self, client, successful_authentication):
        delete_response = client.delete(
            "/categories/11", headers=successful_authentication
        )
        assert delete_response.status_code == 403
