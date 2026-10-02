import input
import output


def main():
	students = [input.input_student_info() for _ in range(input.num_students())]
	courses = [input.courses_info() for _ in range(input.n_courses())]
	marks = input.student_marks(courses, students)

	print("\nCOURSES")
	output.course_print(courses)
	print("\nSTUDENTS")
	output.student_print(students)

	number_of_courses = int(input.read_input("\nEnter the number of courses whose grades you want to see: "))
	for _ in range(number_of_courses):
		course_id = input.read_input("Enter the course ID: ")
		print(f"\nMARKS - {course_id}")
		output.display_marks(marks, students, course_id)

	print("\nRANKING BY GPA")
	output.show_ranking(students, marks, courses)


if __name__ == "__main__":
	main()