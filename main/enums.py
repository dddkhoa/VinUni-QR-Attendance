from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class Role(Enum):
    INSTRUCTOR = "urn:lti:role:ims/lis/Instructor"
    TA = "urn:lti:role:ims/lis/TeachingAssistant"
    SCHOOL_ADMIN = "urn:lti:instrole:ims/lis/Administrator"
    SITE_ADMIN = "urn:lti:sysrole:ims/lis/SysAdmin"
    STUDENT = "urn:lti:role:ims/lis/Learner"

    @classmethod
    def can_grade(cls):
        return [cls.INSTRUCTOR, cls.TA, cls.SCHOOL_ADMIN, cls.SITE_ADMIN]



