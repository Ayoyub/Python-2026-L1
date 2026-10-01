import math
import numpy as np
import curses


def num_students():
    n_students = int(input("Enter the number of student in your class: "))
    return n_students


def students_info(n_students):
    stu_info = []
    for _ in range(n_students):
        id = input("Enter students ID: ")
        name = input("Enter students name: ")
        dob = input("Enter students DoB (DD/MM/YYYY): ")
        stu_info.append({"id": id, "name": name, "dob": dob})
    return stu_info


def n_courses():
    return int(input("Enter the number of courses: "))

def courses_info(nb_courses):
    cou_info = []
    for _ in range(nb_courses):
        id = input("Enter course ID: ")
        name = input("Enter courses name: ")
        credits = int(input("Enter course credits: "))
        cou_info.append({"id": id, "name": name, "credits": credits})
    return cou_info


def get_name(student_id, students):
    for student in students:
        if student["id"] == student_id:
            return student["name"]
    return None


def selec_course():
    marks = []
    num = int(input("Enter the number of courses you want to grade: "))
    for i in range(num):
        found2 = False
        id_course = input("Choose the courses ID to grade: ")
        for course in cou_info:
            if id_course == course["id"]:
                found2 = True
                n = int(input("Enter the number of students in course you want to grade: "))
                for j in range(n):
                    id = input("Enter the students ID: ")
                    found = False
                    for student in st:
                        if id == student["id"]:
                            found = True
                            mark = math.floor(float(input("Grade: ")) * 10) / 10
                            marks.append({"course": id_course, "student": id, "mark": mark})
                    if found == False:
                        print("Student not found. ")
        if found2 == False:
            print("Course not found. ")
    return marks


def list_courses():
    for course in cou_info:
        print(course["name"])


def list_students():
    for student in st:
        print(student["name"])


def showMarks():
    nb = int(input("Enter the number of courses which grades you want to see: "))
    for _ in range(nb):
        course_id = input("Enter the courses ID for which you want to see the grades: ")
        found = False
        for course in cou_info:
            if course_id == course["id"]:
                found = True
                for mark in marks:
                    if mark["course"] == course_id:
                        name = get_name(mark["student"], st)
                        print(name, ":", mark["mark"])
        if found == False:
            print("Course not found. ")

def get_credits(course_id):
    for course in cou_info:
        if course["id"] == course_id:
            return course["credits"]
    return 0


def averageGpa(student_id):
    notes = []
    creds = []
    for m in marks:
        if m["student"] == student_id:
            notes.append(m["mark"])
            creds.append(get_credits(m["course"]))
    if not notes or sum(creds) == 0:
        return 0
    notes = np.array(notes)
    creds = np.array(creds)
    return np.sum(notes * creds) / np.sum(creds)

numstu = num_students()
st = students_info(numstu)
nb_courses = n_courses()
cou_info = courses_info(nb_courses)
marks = selec_course()

list_courses()
list_students()
showMarks()