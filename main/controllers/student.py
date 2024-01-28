from flask import request, jsonify
import requests

from main import app, db, qr_secret_key, canvas
from main.commons.decorators import (
    jwt_required,
    validate_input,
)
from main.models.status import StatusModel
from main.schemas.base import PaginationSchema
from main.schemas.student import StudentRecord, StudentRecordList
from main.libs.qr import verify_token


@app.route("/api/qr/scan", methods=["POST"])
def scan_qr():
    data = request.get_json()
    token = data.get("token")
    secret = data.get("secret")

    if verify_token(token, secret):
        requests.post()
        return jsonify({"message": "success"}), 200
    else:
        return jsonify({"message": "failed"}), 400


@app.route("/api/courses/<int:course_id>/students/<int:student_id>/records", methods=["GET"])
# @jwt_required
def get_student_records(course_id, student_id, **__):
    # course = canvas.get(course_id)

    student_statuses = StatusModel.query.filter_by(student_id=student_id, course_id=course_id).all()

    results = {"attendanceRecords": student_statuses}
    response = StudentRecordList().dump(results)
    return response, 200

