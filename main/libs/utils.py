import random
from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import sha512
from os import urandom

import jwt
from pylti1p3.tool_config import ToolConfDict

from main import config
from main.commons.exceptions import ExpiredAccessToken, InvalidAccessToken
from main.models.lti_config import LTIConfig


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


def get_lti_config(iss, client_id):
    lti = LTIConfig.query.filter_by(iss=iss, client_id=client_id).first()

    settings = {
        lti.iss: [
            {
                "client_id": lti.client_id,
                "auth_login_url": lti.auth_login_url,
                "auth_token_url": lti.auth_token_url,
                "auth_audience": "null",
                "key_set_url": lti.key_set_url,
                "key_set": None,
                "deployment_ids": [lti.deployment_id],
            }
        ]
    }

    private_key = lti.private_key_file
    public_key = lti.public_key_file
    tool_conf = ToolConfDict(settings)

    tool_conf.set_private_key(iss, private_key, client_id=client_id)
    tool_conf.set_public_key(iss, public_key, client_id=client_id)

    return tool_conf

