from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class AppRole(Enum):
    INSTRUCTOR = "Instructor"
    LEARNER = "Learner"


class LTIRole(Enum):
    ROLE = "https://purl.imsglobal.org/spec/lti/claim/roles"
    INSTRUCTOR = "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"
    TA = ""
    SCHOOL_ADMIN = ""
    SITE_ADMIN = ""
    LEARNER = "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"

    @classmethod
    def can_grade(cls):
        return [cls.INSTRUCTOR, cls.TA, cls.SCHOOL_ADMIN, cls.SITE_ADMIN]


class StatusType(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class StatusGrade(Enum):
    PRESENT = 1
    ABSENT = 0
    LATE = 0.5
    EXCUSED = None  # TODO: Define logic for EXCUSED


