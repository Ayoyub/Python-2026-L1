import input
import output
from pathlib import Path
import gzip
import shutil
from builtins import input as read_input

DATA_DIR = Path(__file__).resolve().parent
file_path = DATA_DIR / "students.dat"
compressed_file_path = DATA_DIR / "students.dat.gz"


def migrate_legacy_data_file():
	if compressed_file_path.exists() or not file_path.exists():
		return

	try:
		with gzip.open(file_path, "rb") as file:
			file.read(1)
	except (OSError, EOFError):
		return

	file_path.rename(compressed_file_path)


def main():
	migrate_legacy_data_file()

	if compressed_file_path.is_file():
		answer = read_input("Saved data found, do you want to open it? [y/n] ")
		if answer.strip().lower() == "y":
			with gzip.open(compressed_file_path, "rb") as f_in:
				with open(file_path, "wb") as f_out:
					shutil.copyfileobj(f_in, f_out)
			print(f"Saved data was decompressed to {file_path}.")
		return

	students = [input.input_student_info() for _ in range(input.num_students())]
	courses = [input.courses_info() for _ in range(input.n_courses())]
	marks = input.student_marks(courses, students)
	input.save_students(students)
	input.save_courses(courses)
	input.save_marks(marks)
	with gzip.open(compressed_file_path, "wt", encoding="utf-8") as file:
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