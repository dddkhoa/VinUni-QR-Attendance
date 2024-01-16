from main import db


class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    items = db.relationship("ItemModel", back_populates="category")
