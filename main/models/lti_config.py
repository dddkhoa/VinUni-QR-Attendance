import json

from Crypto.PublicKey import RSA
from jwcrypto.jwk import JWK
# from sqlalchemy import event

from main import db, config


class LTIConfig(db.Model):
    __tablename__ = "lti_config"
    id = db.Column(db.Integer, primary_key=True)
    iss = db.Column(db.Text)
    client_id = db.Column(db.Text)
    auth_login_url = db.Column(db.Text)
    auth_token_url = db.Column(db.Text)
    key_set_url = db.Column(db.Text)
    private_key_file = db.Column(db.Text)
    public_key_file = db.Column(db.Text)
    public_jwk = db.Column(db.Text)
    deployment_id = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )


# This event does not work for `flask db upgrade` command, but works for `db.create_all()`
# thus, use this script in migration script instead.
# @event.listens_for(LTIConfig.__table__, 'after_create')
def create_lti_config():
    client_id = config.LTI_CLIENT_ID
    deployment_id = config.LTI_DEPLOYMENT_ID
    print("IN CREATE LTICONFIG")

    print("Starting key generation...")
    key = RSA.generate(4096)
    print("Generating Private Key...")
    private_key = key.exportKey()
    print("Generating Public Key...")
    public_key = key.publickey().exportKey()

    print("Converting Keys to JWKS...")
    jwk_obj = JWK.from_pem(public_key)
    public_jwk = json.loads(jwk_obj.export_public())
    public_jwk["alg"] = "RS256"
    public_jwk["use"] = "sig"
    public_jwk_str = json.dumps(public_jwk)

    if ".test." in config.CANVAS_URL:
        issuer = "https://canvas.test.instructure.com"
    else:
        issuer = "https://canvas.instructure.com"

    lti_config = LTIConfig(
        iss=issuer,
        client_id=client_id,
        auth_login_url=f"{config.CANVAS_URL}/api/lti/authorize_redirect",
        auth_token_url=f"{config.CANVAS_URL}/login/oauth2/token",
        key_set_url=f"{config.CANVAS_URL}/api/lti/security/jwks",
        private_key_file=private_key.decode("utf-8"),
        public_key_file=public_key.decode("utf-8"),
        public_jwk=public_jwk_str,
        deployment_id=deployment_id,
    )

    print(f"JSON url: {config.LTI_URL}/config/{lti_config.id}/json")

    # db.session.add(lti_config)
    # db.session.commit()

    return lti_config
