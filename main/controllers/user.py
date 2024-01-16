from main import app, db
from main.commons.decorators import validate_input
from main.commons.exceptions import EmailAlreadyExists, InvalidEmailOrPassword
from main.libs.utils import generate_jwt_token
from main.models.user import UserModel
from main.schemas.user import LoginUserSchema, RegisterUserSchema


@app.route("/users/signup", methods=["POST"])
@validate_input(RegisterUserSchema)
def sign_up_user(data):
    user = UserModel.query.filter_by(email=data["email"]).one_or_none()
    if user:
        raise EmailAlreadyExists()

    user = UserModel(data["email"], data["password"])
    db.session.add(user)
    db.session.commit()

    jwt_token = generate_jwt_token(user.id)
    return {"access_token": jwt_token}


@app.route("/users/auth", methods=["POST"])
@validate_input(LoginUserSchema)
def authenticate_user(data):
    user = UserModel.query.filter_by(email=data["email"]).one_or_none()

    if user and user.validate_password(data["password"]):
        jwt_token = generate_jwt_token(user.id)
        return {"access_token": jwt_token}
    raise InvalidEmailOrPassword()
