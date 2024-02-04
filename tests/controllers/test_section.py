import pytest


class TestSection:
    def test_get_sections_by_course(self, client):
        course_id = 1

        response = client.get(f'/api/courses/{course_id}/sections/')
        assert response.status_code == 200

    def test_get_dates_by_course(self, client):
        course_id = 1
        section_id = 1

        response = client.get(f'/api/courses/{course_id}/sections/{section_id}/dates/')
        assert response.status_code == 200

    def test_get_section_by_id_with_enrollments(self, client):
        course_id = 1
        section_id = 1

        response = client.get(f'/api/courses/{course_id}/sections/{section_id}')
        assert response.status_code == 200
