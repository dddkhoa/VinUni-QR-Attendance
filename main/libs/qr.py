from io import BytesIO

import pyotp
import qrcode


def generate_secret_key():
    return pyotp.random_base32()


def get_totp_token(secret):
    totp = pyotp.TOTP(secret, interval=5)
    return totp.now()


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)

    return img_buffer


def generate_new_qr_code(qr_secret_key, encoded_message):
    token = get_totp_token(qr_secret_key)
    encoded_message = encoded_message + token
    qr_code_image = generate_qr_code(token)
    return qr_code_image


def verify_token(user_token, secret):
    totp = pyotp.TOTP(secret, interval=5)
    return totp.verify(user_token)
