import pytest

from main import db
from main.libs.utils import generate_jwt_token
from main.models.status import StatusModel


class TestStatus:
    def test_get_students_statuses(self, client):
        course_id = 1
        section_id = 1

        response = client.get(f'/api/courses/{course_id}/sections/{section_id}/statuses')
        assert response.status_code == 200

    def test_get_checkin_qr(self, client):
        course_id = 1

        response = client.get(f'/api/courses/{course_id}/qr')
        assert response.status_code == 200

    def test_create_statuses(self, client):
        course_id = 1
        data = {
            "user_id": 1,
            "qr_decoded_key": "valid_key",
            "date": "2024-02-04"
        }

        response = client.post(f'/api/courses/{course_id}/sections/1/statuses/', json=data)
        assert response.status_code == 200

    def test_update_status(self, client):
        status_id = 1
        data = {
            "status": "present"
        }

        response = client.put(f'/api/statuses/{status_id}', json=data)
        assert response.status_code == 200

    def test_submit_grade(self, client):
        course_id = 1
        student_id = 1
        status_id = 1

        response = client.post(f'/api/courses/{course_id}/students/{student_id}/grades', json={"status_id": status_id})
        assert response.status_code == 200

    def test_submit_grades(self, client):
        course_id = 1
        student_ids = [1, 2, 3]

        response = client.post(f'/api/courses/{course_id}/students/grades', json={"student_ids": student_ids})
        assert response.status_code == 200
