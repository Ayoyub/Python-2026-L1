import math
from pathlib import Path
from builtins import input as read_input
from domains.student import Student
from domains.course import Course

DATA_DIR = Path(__file__).resolve().parent


def num_students():
    return int(read_input("Enter the number of students in your class: "))

def n_courses():
    return int(read_input("Enter the number of courses: "))


def input_student_info():
    student_id = read_input("\tStudent ID: ")
    name = read_input("\tStudent name: ")
    dob = read_input("\tDate of birth (DD/MM/YYYY): ")
    return Student(student_id, name, dob)


def courses_info():
    course_id = read_input("Enter course ID: ")
    name = read_input("Enter course name: ")
    credits = int(read_input("Enter course credits: "))
    return Course(course_id, name, credits)


def student_marks(courses, students):
    marks = []
    number_of_courses = int(read_input("Enter the number of courses to grade: "))
    for _ in range(number_of_courses):
        sel_course_id = read_input("Select a course ID: ")
        course = next((course for course in courses
                       if course.get_id() == sel_course_id), None)
        if course is None:
            print("Course not found.")
            continue

        number_of_students = int(read_input("Enter the number of students to grade: "))
        for _ in range(number_of_students):
            student_id = read_input("Enter the student ID: ")
            student = next((student for student in students
                            if student.get_id() == student_id), None)
            if student is None:
                print("Student not found.")
                continue

            mark = math.floor(float(read_input("Grade: ")) * 10) / 10
            marks.append({"course": course.get_id(), "student": student.get_id(), "mark": mark})
    return marks


def save_students(students):
    with open(DATA_DIR / "students.txt", "w", encoding="utf-8") as file:
        file.write("STUDENTS INFO:\n")
        for student in students:
            file.write(f"{student}\n")


def save_courses(courses):
    with open(DATA_DIR / "courses.txt", "w", encoding="utf-8") as file:
        file.write("COURSES INFO:\n")
        for course in courses:
            file.write(f"{course}\n")


def save_marks(marks):
    with open(DATA_DIR / "marks.txt", "w", encoding="utf-8") as file:
        file.write("MARKS:\n")
        for mark in marks:
            file.write(
                f"Course: {mark['course']} | Student: {mark['student']} | "
                f"Mark: {mark['mark']:.1f}\n"
            )