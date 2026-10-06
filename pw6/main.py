import input
import output
from pathlib import Path
from builtins import input as read_input

DATA_DIR = Path(__file__).resolve().parent


def main():
    # if pickle file exists lodad it
    data = input.load_data()
    if data is not None:
        print(f"Loaded saved data from {input.DATA_FILE.name}.")
        students, courses, marks = data["students"], data["courses"], data["marks"]
    else:
        # if no pickle file, try migrating legacy data
        migrated = input.migrate_legacy_data()
        if migrated is not None:
            students, courses, marks = migrated
        else:
            # still nothing then collect new data
            students = [input.input_student_info()
                        for _ in range(input.num_students())]
            courses = [input.courses_info() for _ in range(input.n_courses())]
            marks = input.student_marks(courses, students)
            input.save_data(students, courses, marks)
            print(f"Data saved to {input.DATA_FILE.name}.")

    output.curses.wrapper(output.menu, students, courses, marks)


if __name__ == "__main__":
    main()