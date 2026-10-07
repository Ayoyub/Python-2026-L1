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