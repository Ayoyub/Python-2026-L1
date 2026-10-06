import input
import output
from pathlib import Path
from builtins import input as read_input

DATA_DIR = Path(__file__).resolve().parent


def main():
    # 1. New pickle-compressed file exists -> load it directly.
    data = input.load_data()
    if data is not None:
        print(f"Loaded saved data from {input.DATA_FILE.name}.")
        students, courses, marks = data["students"], data["courses"], data["marks"]
    else:
        # 2. No new file -> try migrating the legacy text-based data.
        migrated = input.migrate_legacy_data()
        if migrated is not None:
            students, courses, marks = migrated
        else:
            # 3. Nothing to load -> collect fresh data from the user.
            students = [input.input_student_info()
                        for _ in range(input.num_students())]
            courses = [input.courses_info() for _ in range(input.n_courses())]
            marks = input.student_marks(courses, students)
            input.save_data(students, courses, marks)
            print(f"Data saved to {input.DATA_FILE.name}.")

    output.curses.wrapper(output.menu, students, courses, marks)


if __name__ == "__main__":
    main()