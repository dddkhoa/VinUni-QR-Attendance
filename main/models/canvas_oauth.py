from sqlalchemy import Index

from main import db, config


class CanvasOAuth(db.Model):
    __tablename__ = "canvas_oauth"

    canvas_user_id = db.Column(db.BIGINT)
    token = db.Column(db.String(255))
    last_used_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    canvas_user_id_index = Index("idx_canvas_user_id", canvas_user_id)

