import random
from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import sha512
from os import urandom

import jwt

from main import config
from main.commons.exceptions import ExpiredAccessToken, InvalidAccessToken


def generate_random_attendance_key():
    global attendance_secret_key
    attendance_secret_key = random.randint(0, 1000000)
    return attendance_secret_key


def generate_random_salt():
    return b64encode(urandom(64)).decode("utf-8")


def generate_hashed_password(password, salt):
    hashed_password = sha512(f"{password}{salt}".encode())
    return hashed_password.hexdigest()


def generate_jwt_token(user_id):
    payload = {
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "sub": user_id,
    }

    token = jwt.encode(payload=payload, key=config.JWT_SECRET_KEY, algorithm="HS256")

    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(
            jwt=token,
            key=config.JWT_SECRET_KEY,
            algorithms="HS256",
            options={"verify_signature": True, "verify_exp": True},
        )
        return payload["sub"]

    except jwt.ExpiredSignatureError:
        raise ExpiredAccessToken()

    except jwt.InvalidTokenError:
        raise InvalidAccessToken()
