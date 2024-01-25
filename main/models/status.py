from main import db


class StatusModel(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    class_date = db.Column(db.Date, nullable=False)
    section_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.Boolean, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    # account_id = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, nullable=False)
    # tool_consumer_instance_guid = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    @classmethod
    def initialize_list(
        cls, session, section, class_date, teacher_id, tool_consumer_instance_guid
    ):
        statuses = cls.existing_for_course_and_date(
            session, section.course_id, class_date, tool_consumer_instance_guid
        )
        lookup_table = cls.key_statuses_by_student_id(statuses, section.id)
        students_table = {}

        for student in section.students:
            students_table[student.id] = student
            if student.id not in lookup_table:
                default_status = cls(
                    student_id=student.id,
                    section_id=section.id,
                    course_id=section.course_id,
                    class_date=class_date,
                    teacher_id=teacher_id,
                    tool_consumer_instance_guid=tool_consumer_instance_guid,
                    fixed=True,
                )
                statuses.append(default_status)

        for status in statuses:
            status.student = students_table.get(status.student_id)

        statuses = [status for status in statuses if status.student is not None]
        return sorted(statuses, key=lambda status: status.student.sortable_name)

    @classmethod
    def existing_for_course_and_date(
        cls, session, course_id, class_date, tool_consumer_instance_guid
    ):
        return (
            session.query(cls)
            .filter_by(
                course_id=course_id,
                class_date=class_date,
                tool_consumer_instance_guid=tool_consumer_instance_guid,
            )
            .all()
        )

    @classmethod
    def key_statuses_by_student_id(cls, statuses, section_id):
        return {
            status.student_id: status
            for status in statuses
            if status.section_id == section_id
        }
