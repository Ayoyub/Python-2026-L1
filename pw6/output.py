import pandas as pd
import numpy as np
from pathlib import Path
from builtins import input as read_input


def student_print(students):
    data = [
        {"ID": s.get_id(), "Name": s.get_name(), "DoB": s.get_dob()}
        for s in students
    ]
    df = pd.DataFrame(data)
    print(df.to_string(index=False))


def course_print(courses):
    data = [
        {"ID": c.get_id(), "Name": c.get_name(), "Credits": c.get_credits()}
        for c in courses
    ]
    df = pd.DataFrame(data)
    print(df.to_string(index=False))


def display_marks(marks, students, course_id):
    student_names = {s.get_id(): s.get_name() for s in students}
    marks_df = pd.DataFrame(marks)
    matching = marks_df[marks_df["course"] == course_id]
    if matching.empty:
        print("No marks found for this course.")
        return
    matching = matching.rename(columns={"student": "ID", "mark": "Grade"})
    matching["Name"] = matching["ID"].map(student_names).fillna("Unknown student")
    print(matching[["Name", "Grade"]].to_string(index=False))


def show_ranking(students, marks, courses):
    credits = {c.get_id(): c.get_credits() for c in courses}
    credits_arr = np.array([credits.get(m["course"], 0) for m in marks])
    marks_arr = np.array([m["mark"] for m in marks])

    ranking = []
    for student in students:
        sid = student.get_id()
        mask = np.array([m["student"] == sid for m in marks])
        student_marks_arr = marks_arr[mask]
        student_credits_arr = credits_arr[mask]
        total_credits = float(np.sum(student_credits_arr))
        if total_credits > 0:
            gpa = float(np.sum(student_marks_arr * student_credits_arr) / total_credits)
        else:
            gpa = 0.0
        ranking.append({"ID": sid, "Name": student.get_name(), "GPA": gpa})

    df = pd.DataFrame(ranking).sort_values("GPA", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    print(df.to_string())