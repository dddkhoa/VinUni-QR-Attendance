from main import app, canvas
from main.schemas.section import SectionSchema, SectionListSchema


@app.route("/courses/<int:course_id>/sections/", methods=["GET"])
def get_sections_by_course(course_id, **__):
    course = canvas.get_course(course_id)
    sections = course.get_sections()
    response = SectionListSchema().dump(sections)
    return response


@app.route("/courses/<int:course_id>/sections/<int:section_id>", methods=["GET"])
def get_section_by_id_with_enrollments(course_id, section_id, **__):
    course = canvas.get_course(course_id)
    section = course.get_section(section_id, include=["students", "avatar_url"])
    response = SectionSchema().dump(section)

    return response
