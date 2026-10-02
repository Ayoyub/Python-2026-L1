import input
import output
from pathlib import Path
import gzip
DATA_DIR = Path(__file__).resolve().parent

def main():
	students = [input.input_student_info() for _ in range(input.num_students())]
	courses = [input.courses_info() for _ in range(input.n_courses())]
	marks = input.student_marks(courses, students)
	input.save_students(students)
	input.save_courses(courses)
	input.save_marks(marks)
	with gzip.open(DATA_DIR / "output.dat", "wt", encoding="utf-8") as file:
		file.write("STUDENTS INFO:\n")
		for student in students:
			file.write(f"{student}\n")
		file.write("\nCOURSES INFO:\n")
		for course in courses:
			file.write(f"{course}\n")
		file.write("\nMARKS:\n")
		for mark in marks:
			file.write(
				f"Course: {mark['course']} | Student: {mark['student']} | "
				f"Mark: {mark['mark']:.1f}\n"
			)
	output.curses.wrapper(output.menu, students, courses, marks)

		

if __name__ == "__main__":
	main()