import curses


def student_print(students):
    for student in students:
        print(f"{student.get_id()} - {student.get_name()} (born {student.get_dob()})")

def course_print(courses):
    for course in courses:
        print(f"{course.get_id()} - {course.get_name()} ({course.get_credits()} credits)")

def display_marks(marks, students, course_id):
    student_names = {student.get_id(): student.get_name() for student in students}
    matching_marks = [mark for mark in marks if mark["course"] == course_id]
    if not matching_marks:
        print("No marks found for this course.")
        return
    for mark in matching_marks:
        print(f"{student_names.get(mark['student'], 'Unknown student')}: {mark['mark']:.1f}")


def show_ranking(students, marks, courses):
    credits = {course.get_id(): course.get_credits() for course in courses}
    ranking = []
    for student in students:
        student_marks = [mark for mark in marks if mark["student"] == student.get_id()]
        total_credits = sum(credits.get(mark["course"], 0) for mark in student_marks)
        weighted_marks = sum(mark["mark"] * credits.get(mark["course"], 0)
                             for mark in student_marks)
        gpa = weighted_marks / total_credits if total_credits else 0
        ranking.append((student, gpa))

    for rank, (student, gpa) in enumerate(sorted(ranking, key=lambda item: item[1], reverse=True), 1):
        print(f"{rank}. {student.get_name()} : {gpa:.2f}")


def draw_title(stdscr, title):
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, title.center(max(width - 1, 1))[:width - 1],
                  curses.color_pair(1) | curses.A_BOLD)


def show_page(stdscr, title, lines):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    draw_title(stdscr, title)
    for index, line in enumerate(lines[:max(height - 5, 0)]):
        stdscr.addstr(2 + index, 2, line[:max(width - 4, 1)], curses.color_pair(3))
    if height >= 2:
        stdscr.addstr(height - 2, 2, "Press any key to go back", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()


def page_courses(stdscr, courses, _students, _marks):
    lines = [f"{course.get_id()} - {course.get_name()} ({course.get_credits()} credits)"
             for course in courses]
    show_page(stdscr, "COURSES", lines)


def page_students(stdscr, _courses, students, _marks):
    lines = [f"{student.get_id()} - {student.get_name()} (born {student.get_dob()})"
             for student in students]
    show_page(stdscr, "STUDENTS", lines)


def ask(stdscr, prompt):
    curses.echo()
    curses.curs_set(1)
    stdscr.addstr(2, 2, prompt)
    stdscr.refresh()
    value = stdscr.getstr().decode()
    curses.noecho()
    curses.curs_set(0)
    return value


def page_marks(stdscr, courses, students, marks):
    stdscr.clear()
    draw_title(stdscr, "MARKS BY COURSE")
    course_id = ask(stdscr, "Course ID: ")
    valid_course = any(course.get_id() == course_id for course in courses)
    student_names = {student.get_id(): student.get_name() for student in students}
    lines = [f"{student_names.get(mark['student'], 'Unknown student')}: {mark['mark']:.1f}"
             for mark in marks if mark["course"] == course_id]
    if not valid_course:
        lines = ["Course not found."]
    elif not lines:
        lines = ["No marks found for this course."]
    show_page(stdscr, f"MARKS - {course_id}", lines)


def page_ranking(stdscr, courses, students, marks):
    credits = {course.get_id(): course.get_credits() for course in courses}
    ranking = []
    for student in students:
        student_marks = [mark for mark in marks if mark["student"] == student.get_id()]
        total_credits = sum(credits.get(mark["course"], 0) for mark in student_marks)
        weighted_marks = sum(mark["mark"] * credits.get(mark["course"], 0)
                             for mark in student_marks)
        gpa = weighted_marks / total_credits if total_credits else 0
        ranking.append((student, gpa))
    lines = [f"{rank}. {student.get_name()} : {gpa:.2f}"
             for rank, (student, gpa) in enumerate(
                 sorted(ranking, key=lambda item: item[1], reverse=True), 1)]
    show_page(stdscr, "RANKING BY GPA", lines)


def menu(stdscr, students, courses, marks):
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
        for index, (label, _action) in enumerate(options):
            attribute = curses.color_pair(2) | curses.A_BOLD if index == current else 0
            prefix = "> " if index == current else "  "
            stdscr.addstr(3 + index, 4, prefix + label, attribute)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current = (current - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            action = options[current][1]
            if action is None:
                return
            action(stdscr, courses, students, marks)