import pytest


class TestStudent:
    def test_scan_qr_success(self, client):
        data = {"token": "valid_token", "secret": "valid_secret"}
        response = client.post("/api/qr/scan", json=data)
        assert response.status_code == 200
        assert "success" in response.get_json()["message"]

    def test_scan_qr_failure(self, client):
        data = {"token": "invalid_token", "secret": "invalid_secret"}
        response = client.post("/api/qr/scan", json=data)
        assert response.status_code == 400
        assert "failed" in response.get_json()["message"]

    def test_get_student_records(self, client):
        course_id = 1
        student_id = 1

        response = client.get(f'/api/courses/{course_id}/students/{student_id}/records')
        assert response.status_code == 200
