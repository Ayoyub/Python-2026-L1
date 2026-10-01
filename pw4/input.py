import math
from domains.student import Student
from domains.course import Course

def num_students():
    return int(input("Enter the number of student in your class: ")) 

def n_courses():
    return int(input("Enter the number of courses: "))


def input_student_info():
    id = input("\tStudent's ID is: ")
    name = input("\tYour name: ")
    dob = input("\tDate of birth: ")
    return Student(id, name, dob)


def courses_info():
        id = input("Enter course ID: ")
        name = input("Enter courses name: ")
        return Course(id, name)


def student_marks(courses, students):
    sel_course_id = input("Select a course ID: ")
    for course in courses:
        if course.get_id() == sel_course_id:
            m = {"Course": course.get_name(), "Students and marks": []}
            print("Course name: " + course.get_name() + "\n")
            for student in students:
                mark = float(input("\tEnter " + student.get_name() + "'s mark "))
                mark = math.floor(mark * 10) / 10
                m["Students and marks"].append((student.get_name(), mark))
                return m
    print("Course not found.")
    return None