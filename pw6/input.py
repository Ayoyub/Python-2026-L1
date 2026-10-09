import math
import pickle
import gzip
import tempfile
import re
import shutil
import pandas as po
from pathlib import Path
from builtins import input as read_input
from domains.student import Student
from domains.course import Course

DATA_DIR = Path(__file__).resolve().parent
DATA_FILE = DATA_DIR / "data.pkl.gz"
LEGACY_FILE = DATA_DIR / "students.dat.gz"
LEGACY_PLAIN = DATA_DIR / "students.dat"
BACKUP_DIR = DATA_DIR / "backup"


def num_students():
    return int(read_input("Enter the number of students in your class: "))


def n_courses():
    return int(read_input("Enter the number of courses: "))


def input_student_info():
    student_id = read_input("\tStudent ID: ")
    name = read_input("\tStudent name: ")
    dob = read_input("\tDate of birth (DD/MM/YYYY): ")
    return Student(student_id, name, dob)


def courses_info():
    course_id = read_input("Enter course ID: ")
    name = read_input("Enter course name: ")
    credits = int(read_input("Enter course credits: "))
    return Course(course_id, name, credits)


def student_marks(courses, students):
    import pandas as pd
    marks = []
    number_of_courses = int(read_input("Enter the number of courses to grade: "))
    for _ in range(number_of_courses):
        sel_course_id = read_input("Select a course ID: ")
        course = next((course for course in courses
                       if course.get_id() == sel_course_id), None)
        if course is None:
            print("Course not found.")
            continue

        number_of_students = int(read_input("Enter the number of students to grade: "))
        for _ in range(number_of_students):
            student_id = read_input("Enter the student ID: ")
            student = next((student for student in students
                            if student.get_id() == student_id), None)
            if student is None:
                print("Student not found.")
                continue

            mark = math.floor(float(read_input("Grade: ")) * 10) / 10
            marks.append({"course": course.get_id(), "student": student.get_id(), "mark": mark})

    # Build DataFrame ONCE, after all marks are collected
    df = pd.DataFrame(marks)
    df.to_csv(DATA_DIR / "marks.csv", index=False)
    print(f"Saved {len(marks)} marks to marks.csv")
    return marks


def save_data(students, courses, marks):
    """Serialize the whole dataset to a single pickle stream, gzip-compressed.
    Writes to a temp file first, then moves atomically (PDF 4: temp files).
    """
    data = {"students": students, "courses": courses, "marks": marks}
    tmp_path = None
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".tmp", delete=False, dir=str(DATA_DIR)) as tmp:
        tmp_path = Path(tmp.name)
    try:
        with gzip.open(tmp_path, "wb") as file:
            pickle.dump(data, file)
        # Remove existing file first to avoid Windows lock issues
        if DATA_FILE.exists():
            DATA_FILE.unlink()
        tmp_path.rename(DATA_FILE)
    except Exception:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
            raise


def backup():
    """Create a timestamped backup in backup/ directory (PDF 4: directories + shutil)."""
    if not DATA_FILE.exists():
        return
    BACKUP_DIR.mkdir(exist_ok=True)
    import datetime
    ts = datetime.datetime.fromtimestamp(DATA_FILE.stat().st_mtime)
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / f"data_backup_{ts_str}.pkl.gz"
    shutil.copy2(DATA_FILE, dest)
    print(f"Backup saved to {dest.name}")


def load_data():
    """Load the pickle-compressed dataset. Returns None if no file exists."""
    if not DATA_FILE.exists():
        return None
    with gzip.open(DATA_FILE, "rb") as file:
        return pickle.load(file)


def migrate_legacy_data():
    """Convert the old text-based students.dat(.gz) into the new pickle format.

    Runs once: only when the new data file is absent but a legacy file is present.
    Returns the migrated (students, courses, marks) or None if nothing to migrate.
    """
    if DATA_FILE.exists():
        return None
    legacy = LEGACY_FILE if LEGACY_FILE.exists() else (
        LEGACY_PLAIN if LEGACY_PLAIN.exists() else None)
    if legacy is None:
        return None

    try:
        with gzip.open(legacy, "rt", encoding="utf-8") as file:
            text = file.read()
    except (OSError, EOFError):
        # not actually gzip (plain file) -> read as text
        with open(legacy, "r", encoding="utf-8") as file:
            text = file.read()

    students, courses, marks = _parse_legacy_text(text)
    save_data(students, courses, marks)
    legacy.unlink()
    print(f"Legacy data migrated from {legacy.name} to {DATA_FILE.name}.")
    return students, courses, marks


_LEGACY_MARK_RE = re.compile(
    r"Course:\s*(\S+)\s*\|\s*Student:\s*(\S+)\s*\|\s*Mark:\s*([\d.]+)")


def _parse_legacy_text(text):
    students, courses, marks = [], [], []
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("STUDENTS"):
            section = "students"
            continue
        if line.startswith("COURSES"):
            section = "courses"
            continue
        if line.startswith("MARKS"):
            section = "marks"
            continue

        if section == "students" and line.startswith("ID:"):
            parts = [p.strip() for p in line.split("|")]
            students.append(Student(parts[0][4:], parts[1][6:], parts[2][5:]))
        elif section == "courses" and line.startswith("ID:"):
            parts = [p.strip() for p in line.split("|")]
            courses.append(Course(parts[0][4:], parts[1][6:], int(parts[2][9:])))
        elif section == "marks":
            m = _LEGACY_MARK_RE.match(line)
            if m:
                marks.append({"course": m.group(1), "student": m.group(2),
                              "mark": float(m.group(3))})
    return students, courses, marks