class Student:
    def __init__(self, student_id, name, dob):
        self._id = student_id
        self._name = name
        self._dob = dob

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_dob(self):
        return self._dob

    def __str__(self):
        return f"ID: {self._id} | Name: {self._name} | DoB: {self._dob}"