
import requests
from flask import request


from main import app, config
from main.libs.canvas_helper import HttpCanvasAuthorizedRequest
from main.schemas.section import SectionSchema, SectionListSchema


@app.route("/courses/<int:course_id>/sections/", methods=["GET"])
def get_sections_by_course(course_id, **__):
    query = {"include": ["students", "avatar_url"]}

    endpoint = f"/api/v1/courses/{course_id}/sections"

    canvas_request = HttpCanvasAuthorizedRequest(config, endpoint, query)

    sections = canvas_request.send_request()
    response = SectionListSchema().dump(sections)

    return response


@app.route("/courses/<int:course_id>/sections/<int:section_id>", methods=["GET"])
def get_section_by_id_with_enrollments(course_id, section_id, **__):
    query = {"include": ["students", "avatar_url"]}

    endpoint = f"/api/v1/courses/{course_id}/sections/{section_id}"

    canvas_request = HttpCanvasAuthorizedRequest(config, endpoint, query)

    section = canvas_request.send_request()
    response = SectionSchema().dump(section)

    return response

