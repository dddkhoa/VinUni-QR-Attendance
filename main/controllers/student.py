from flask import request, jsonify
import requests

from main import app, db, qr_secret_key
from main.commons.decorators import (
    jwt_required,
    validate_input,
)
from main.schemas.base import PaginationSchema
from main.schemas.student import StudentSchema, StudentListSchema
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



