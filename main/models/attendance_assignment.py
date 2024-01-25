

from canvasapi import Canvas

from main import db, config
from main.enums import StatusType, StatusGrade
from main.models.status import StatusModel


class AttendanceAssignment:
    def __init__(self, canvas: Canvas, course_id, assignment_name, tool_launch_url=config.LTI_URL):
        self.canvas = canvas
        self.course_id = course_id
        self.tool_launch_url = tool_launch_url

        self.course = canvas.get_course(self.course_id)
        self.assignments = self.course.get_assignments()

        self.assignment = None
        for assignment in self.assignments:
            if assignment.name == assignment_name:
                self.assignment = assignment
                self.max_point = self.assignment.points_possible

    def get_student_grade(self, student_id):
        section_id = StatusModel.query.filter_by(student_id=student_id,
                                                 course_id=self.course_id).first().section_id

        student_statuses = StatusModel.query.filter_by(student_id=student_id,
                                                       course_id=self.course_id,
                                                       section_id=section_id).all()
        total_attendances = len(student_statuses)

        present_count = StatusModel.query.filter_by(student_id=student_id,
                                                    section_id=section_id,
                                                    course_id=self.course_id,
                                                    attendance=StatusType.PRESENT.value).count()

        late_count = StatusModel.query.filter_by(student_id=student_id,
                                                 course_id=self.course_id,
                                                 section_id=section_id,
                                                 attendance=StatusType.LATE.value).count()

        student_grade = (present_count * StatusGrade.PRESENT.value + late_count * StatusGrade.LATE.value)
        student_grade /= total_attendances
        student_grade *= self.max_point

        return student_grade

    def get_student_grades(self, student_ids):
        grades = {}
        for student_id in student_ids:
            grades[student_id] = self.get_student_grade(student_id)
        return grades

    def submit_grade(self, student_id):
        grade = self.get_student_grade(student_id)
        submission = self.assignment.get_submission(student_id)
        submission.edit(submission={'posted_grade': grade,
                                    'submission_type': 'basic_lti_launch',
                                    'url': self.tool_launch_url})

    def submit_grades(self, student_ids):
        grades = self.get_student_grades(student_ids)
        for student_id in student_ids:
            grade = grades[student_id]
            submission = self.assignment.get_submission(student_id)
            submission.edit(submission={'posted_grade': grade,
                                        'submission_type': 'basic_lti_launch',
                                        'url': self.tool_launch_url})
