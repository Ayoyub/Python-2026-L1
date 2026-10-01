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


def get_credits(course_id):
    for course in cou_info:
        if course["id"] == course_id:
            return course["credits"]
    return 0


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


def sort_students_by_gpa():
    for student in st:
        student["gpa"] = averageGpa(student["id"])
    st.sort(key=lambda s: s["gpa"], reverse=True)


def show_ranking():
    print("\nRanking by GPA (descending):")
    for rank, student in enumerate(st, start=1):
        print(f"{rank}. {student['name']} : {student['gpa']:.2f}")





"""

UI


ngl i asked AI to help me to understand how curses work 

"""



def draw_title(stdscr, title):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, 0, title.center(w - 1)[:w - 1])
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)


def ask(stdscr, y, x, prompt):
    curses.echo()
    curses.curs_set(1)
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    value = stdscr.getstr().decode()
    curses.noecho()
    curses.curs_set(0)
    return value


def show_page(stdscr, title, lines):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    draw_title(stdscr, title)
    for i, line in enumerate(lines[:h - 5]):
        stdscr.addstr(2 + i, 2, line[:w - 4], curses.color_pair(3))
    stdscr.addstr(h - 2, 2, "Press any key to go back", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()


def page_courses(stdscr):
    lines = [f"{c['id']} - {c['name']} ({c['credits']} credits)" for c in cou_info]
    show_page(stdscr, "COURSES", lines)


def page_students(stdscr):
    lines = [f"{s['id']} - {s['name']} (born {s['dob']})" for s in st]
    show_page(stdscr, "STUDENTS", lines)


def page_marks(stdscr):
    stdscr.clear()
    draw_title(stdscr, "MARKS BY COURSE")
    course_id = ask(stdscr, 2, 2, "Course ID: ")
    lines = []
    for m in marks:
        if m["course"] == course_id:
            lines.append(f"{get_name(m['student'], st)} : {m['mark']}")
    if not lines:
        lines = ["Course not found or no marks."]
    show_page(stdscr, "MARKS - " + course_id, lines)


def page_ranking(stdscr):
    sort_students_by_gpa()
    lines = [f"{rank}. {s['name']} : {s['gpa']:.2f}"
             for rank, s in enumerate(st, start=1)]
    show_page(stdscr, "RANKING BY GPA", lines)


def menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    options = [
        ("List courses", page_courses),
        ("List students", page_students),
        ("Show marks of a course", page_marks),
        ("Ranking by GPA", page_ranking),
        ("Quit", None),
    ]
    current = 0

    while True:
        stdscr.clear()
        draw_title(stdscr, "STUDENT MARK MANAGEMENT")
        for i, (label, _) in enumerate(options):
            if i == current:
                stdscr.addstr(3 + i, 4, "> " + label, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(3 + i, 4, "  " + label)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current = (current - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            action = options[current][1]
            if action is None:
                break
            action(stdscr)






numstu = num_students()
st = students_info(numstu)
nb_courses = n_courses()
cou_info = courses_info(nb_courses)
marks = selec_course()

list_courses()
list_students()
showMarks()

sort_students_by_gpa()
show_ranking()


curses.wrapper(menu)




