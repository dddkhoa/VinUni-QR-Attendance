from sqlalchemy import event
from sqlalchemy.orm import validates

from main import db


class CourseConfig(db.Model):
    __tablename__ = "course_configs"

    course_id = db.Column(db.Integer, primary_key=True)
    tool_consumer_instance_guid = db.Column(db.String(256))
    tardy_weight = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    @validates("course_id", "tool_consumer_instance_guid")
    def validate_not_null(self, key, value):
        assert value is not None, f"{key} cannot be null"
        return value

    @validates("tardy_weight")
    def validate_tardy_weight(self, key, value):
        if value is not None:
            assert 0 <= value <= 1, "tardy_weight must be between 0 and 1"
        return value

    @staticmethod
    def after_save(mapper, connection, target):
        target.needs_regrade = (
            target.tardy_weight is not None and "tardy_weight" in target.__dict__
        ) or "omit_from_final_grade" in target.__dict__

    @property
    def needs_regrade(self):
        return getattr(self, "_needs_regrade", False)

    @needs_regrade.setter
    def needs_regrade(self, value):
        self._needs_regrade = value


event.listen(CourseConfig, "after_insert", CourseConfig.after_save)
event.listen(CourseConfig, "after_update", CourseConfig.after_save)
