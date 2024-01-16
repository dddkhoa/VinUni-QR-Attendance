from main import db


class ItemModel(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("CategoryModel", back_populates="items")
