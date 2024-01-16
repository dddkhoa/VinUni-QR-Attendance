class Student:
    def __init__(self, params):
        self.id = params.get("id")
        self.name = params.get("name")
        self.sortable_name = params.get("sortable_name")
        self.sis_id = params.get("sis_id")
        self.avatar_url = params.get("avatar_url")
        self.active = self.check_for_active_enrollments(params.get("enrollments"))

    def as_json(self):
        # Python's integer size is not limited like JavaScript's,
        # but if the ID needs to be a string, so we convert it here
        return {
            "id": str(self.id),
            "name": self.name,
            "sortable_name": self.sortable_name,
            "avatar_url": self.avatar_url,
        }

    @classmethod
    def list_from_params(cls, list=[]):
        return [cls(params) for params in list]

    @classmethod
    def active_list_from_params(cls, list=[]):
        return [student for student in cls.list_from_params(list) if student.active]

    def check_for_active_enrollments(self, enrollments):
        if enrollments is None:
            return True
        return any(
            e.get("enrollment_state") in ["active", "invited"] for e in enrollments
        )
