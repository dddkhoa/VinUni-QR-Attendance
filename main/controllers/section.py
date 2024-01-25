from flask import session, request

from main import app, canvas
from main.commons.decorators import jwt_required
from main.models.status import StatusModel
from main.schemas.section import SectionSchema, SectionListSchema


@app.route("/api/courses/<int:course_id>/sections/", methods=["GET"])
# @jwt_required
def get_sections_by_course(course_id, **__):
    course = canvas.get_course(course_id)
    sections = course.get_sections()
    results = {'sections': []}
    for section in sections:
        results['sections'].append(SectionSchema().dump(section))

    response = SectionListSchema().dump(results)
    return response


@app.route("/api/courses/<int:course_id>/dates/", methods=["GET"])
def get_dates_by_course(course_id, **__):
    statuses = StatusModel.query.filter_by(course_id=course_id).all()
    class_dates = set(status.class_date for status in statuses)
    response = {"class_dates": list(class_dates)}
    return response


@app.route("/api/courses/<int:course_id>/sections/<int:section_id>", methods=["GET"])
# @jwt_required
def get_section_by_id_with_enrollments(course_id, section_id, **__):
    data = dict(request.args)

    course = canvas.get_course(course_id)
    section = course.get_section(section_id, include=["students", "avatar_url"])
    response = SectionSchema().dump(section)

    return response
