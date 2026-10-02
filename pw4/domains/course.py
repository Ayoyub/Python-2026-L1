class Course:
    def __init__(self, course_id, name, credits):
        self._id = course_id
        self._name = name
        self._credits = credits

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_credits(self):
        return self._credits

    def __str__(self):
        return f"ID: {self._id} | Name: {self._name} | Credits: {self._credits}"