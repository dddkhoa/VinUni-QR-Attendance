from flask import send_file, request
import time
import requests

from main import app, config, db, qr_secret_key
from main.commons.decorators import (
    jwt_required,
    validate_input,
)
from main.controllers.section import get_section_by_id_with_enrollments
from main.libs.qr import generate_new_qr_code


# from main.schemas.base import PaginationSchema
from main.schemas.checkin import QRSchema


@app.route("/api/instructors/qr/generate", methods=["GET"])
@validate_input(QRSchema)
def get_checkin_qr():
    qr_code_image = generate_new_qr_code(qr_secret_key)

    return send_file(qr_code_image, mimetype="image/png")


# @app.route()
# def finish_checkin_session():
#     # Retrieve all attendance status for today session
#     # Fill in the lacking status
#     section_info = get_section_by_id_with_enrollments()
#     pass


@app.route("/api/instructors/attendance/", methods=["GET"])
def get_attendance():
    pass


@app.route("api/instructors/attendance/edit", methods=["PUT"])
def edit_attendance():
    data = request.get_json()


