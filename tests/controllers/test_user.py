import pytest


class TestUser:
    def test_successful_sign_up(self, client):
        data = {"email": "d@gmail.com", "password": "Abc123"}
        response = client.post("/users/signup", json=data)
        assert response.status_code == 200

    def test_successful_auth(self, client):
        data = {"email": "a@gmail.com", "password": "Abc123"}
        response = client.post("/users/auth", json=data)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "email, password",
        [
            ("a@gmail.com", "Abc123"),  # Email already exists
            ("agmail.com", "some_password"),  # Invalid email format
            ("a@gmailcom", "Abc123"),  # Invalid email format
            ("d@gmail.com", "abc123"),  # Password lacks uppercase
            ("d@gmail.com", "Abcdef"),  # Password lacks number
            ("d@gmail.com", "123456"),  # Password lacks character
            ("d@gmail.com", "ABC123"),  # Password lacks lowercase
            ("d@gmail.com", "Ab123"),  # Password len < 6
            ("", ""),  # Invalid email, password
        ],
    )
    def test_invalid_sign_up(self, client, email, password):
        data = {"email": email, "password": password}
        response = client.post("/users/signup", json=data)
        assert response.status_code == 400

    def test_non_json_sign_up(self, client):
        response = client.post("/users/signup")
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "email, password",
        [
            ("a@gmail.com", "wrong_password"),  # Wrong password
            ("a@gmail.com", ""),  # Missing password
            ("agmail.com", "some_password"),  # Invalid email format (Lack "@")
            ("a@gmailcom", "some_password"),  # Invalid email format (Lack "."
            ("d@gmail.com", "some_password"),  # Unregistered user
            ("", ""),  # Invalid email & password
        ],
    )
    def test_invalid_auth(self, client, email, password):
        data = {"email": email, "password": password}
        response = client.post("/users/auth", json=data)
        assert response.status_code == 400
