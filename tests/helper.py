from main import db
from main.models.status import StatusModel


def setup_db():
    setup_status()


def setup_status():
    statuses = [
        StatusModel(
            date="2021-01-01",
            status="PRESENT",
            student_id=1,
            section_id=1,
            course_id=1,
        ),
        StatusModel(
            date="2021-01-01",
            status="PRESENT",
            student_id=2,
            section_id=1,
            course_id=1,
        ),
        StatusModel(
            date="2021-01-01",
            status="PRESENT",
            student_id=3,
            section_id=1,
            course_id=1,
        ),
        StatusModel(
            date="2021-01-01",
            status="PRESENT",
            student_id=4,
            section_id=1,
            course_id=1,
        ),
        StatusModel(
            date="2021-01-01",
            status="PRESENT",
            student_id=5,
            section_id=1,
            course_id=1,
        ),
    ]

    for st in statuses:
        db.session.add(st)

    db.session.commit()
