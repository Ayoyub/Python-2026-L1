import input
import output


def main():
	students = [input.input_student_info() for _ in range(input.num_students())]
	courses = [input.courses_info() for _ in range(input.n_courses())]
	marks = input.student_marks(courses, students)
	output.curses.wrapper(output.menu, students, courses, marks)


if __name__ == "__main__":
	main()