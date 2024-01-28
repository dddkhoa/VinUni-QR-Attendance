import datetime
from flask import request

from main import app, db, config, canvas
from main.commons.decorators import (
    jwt_required,
    validate_input
)
from main.models.status import StatusModel
from main.models.attendance_assignment import AttendanceAssignment
from main.schemas.base import PaginationSchema
from main.schemas.section import SectionSchema
from main.schemas.status import StatusSchema, StatusListSchema, StatusUpdateSchema, StudentStatusDateListSchema


def get_students_section(course_id, section_id):
    course = canvas.get_course(course_id)
    section = course.get_section(section_id, include=["students", "avatar_url"])
    results = SectionSchema().dump(section)
    return results


@app.route("/api/courses/<int:course_id>/sections/<int:section_id>/statuses", methods=["GET"])
# @jwt_required
def get_students_statuses(course_id, section_id, **__):
    data = request.args
    date = data.get("date", None)
    if date:
        date = datetime.datetime.strptime(date, "%d-%m-%Y").date()

    query = {"course_id": course_id, "section_id": section_id, "date": date}
    statuses = StatusModel.query.filter_by(**query).all()
    students = get_students_section(course_id, section_id)["students"]

    student_statuses = []

    for status in statuses:
        for student in students:
            if status.student_id == student['id']:
                student_status = {'email': student['login_id'], 'imageUrl': student['avatar_url'],
                                  'name': student['name'], 'id': status.id, 'status': status.status,
                                  'section': status.section_id}
                student_statuses.append(student_status)

    results = {'date': date, 'students': student_statuses}

    response = StudentStatusDateListSchema().dump(results)
    return response


@app.route("/api/statuses/", methods=["POST"])
# @jwt_required
@validate_input(StatusListSchema)
def create_statuses(data, **__):
    statuses = data.get("statuses", [])
    for status in statuses:
        temp_status = StatusModel(**status)
        db.session.add(temp_status)

    db.session.commit()
    return {}


@app.route("/api/statuses/<int:status_id>", methods=["PUT"])
# @jwt_required
# @validate_input(StatusUpdateSchema)
def update_status(status_id, **__):
    data = request.get_json()
    status = StatusModel.query.filter_by(id=status_id).one_or_none()
    updated_status = {"status": data["status"]}
    if status:
        status.query.filter_by(id=status_id).update(updated_status)
        db.session.commit()

        submit_grade(status.course_id, status.student_id, status.id)

        # submit_grades()
        return {}
    else:
        return {"message": "Status not found"}, 404


@app.route("/api/courses/<int:course_id>/students/<int:student_id>/grades", methods=["POST"])
# @jwt_required
def submit_grade(course_id, student_id, status_id, **__):
    student = StatusModel.query.filter_by(student_id=student_id, course_id=course_id, id=status_id).one_or_none()
    if not student:
        return {"message": "Student not found"}, 404
    attendance_assignment = AttendanceAssignment(canvas, course_id, config.LTI_TOOL_NAME)
    attendance_assignment.submit_grade(student_id)
    return {}


@app.route("/api/courses/<int:course_id>/students/grades", methods=["POST"])
# @jwt_required
def submit_grades(course_id, **__):
    # TODO: need efficient way to create/cache attendance_assignment object
    data = request.get_json()
    student_ids = data.get("student_ids", [])
    attendance_assignment = AttendanceAssignment(canvas, course_id, config.LTI_TOOL_NAME)
    attendance_assignment.submit_grades(student_ids)
    return {}
