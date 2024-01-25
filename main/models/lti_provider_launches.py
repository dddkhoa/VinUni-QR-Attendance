from sqlalchemy import Index

from main import db, config


class LTIProviderLaunch(db.Model):
    __tablename__ = "lti_provider_launch"

    canvas_url = db.Column(db.String(255), nullable=False)
    nonce = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    nonce_index = Index("idx_nonce", nonce)

