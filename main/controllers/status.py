from flask import request

from main import app, db, config, canvas
from main.commons.decorators import (
    jwt_required,
    validate_input
)
from main.models.status import StatusModel
from main.models.attendance_assignment import AttendanceAssignment
from main.schemas.base import PaginationSchema
from main.schemas.status import StatusSchema, StatusListSchema, StatusUpdateSchema


@app.route("/api/courses/<int:course_id>/sections/<int:section_id>/statuses", methods=["GET"])
# @jwt_required
def get_status_for_course_section(course_id, section_id, **__):
    query = {"course_id": course_id, "section_id": section_id}
    statuses = StatusModel.query.filter_by(**query).all()
    print(statuses)
    response = StatusListSchema().dump(statuses)
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
@validate_input(StatusUpdateSchema)
def update_status(status, data, **__):
    if StatusModel.query.filter_by(status_id=status.id).one_or_none():
        status.update(**data)
        db.session.commit()
        submit_grades()
        return {}
    else:
        return {"message": "Status not found"}, 404


@app.route("/api/courses/<int:course_id>/students/<int:student_id>/grades", methods=["POST"])
# @jwt_required
def submit_grade(course_id, student_id, **__):
    student = StatusModel.query.filter_by(student_id=student_id, course_id=course_id).one_or_none()
    if not student:
        return {"message": "Student not found"}, 404
    attendance_assignment = AttendanceAssignment(canvas, course_id, config.LTI_TOOL_NAME)
    attendance_assignment.submit_grade(student_id)
    return {}


@app.route("/api/courses/<int:course_id>/students/grades", methods=["POST"])
# @jwt_required
def submit_grades(course_id, **__):
    data = request.get_json()
    student_ids = data.get("student_ids", [])
    attendance_assignment = AttendanceAssignment(canvas, course_id, config.LTI_TOOL_NAME)
    attendance_assignment.submit_grades(student_ids)
    return {}
