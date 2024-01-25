from main import db


class StatusModel(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    class_date = db.Column(db.Date, nullable=False)
    section_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
