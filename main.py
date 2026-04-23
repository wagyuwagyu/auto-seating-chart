# Importing necessary libraries and modules
import re
import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap import Style


root = tk.Tk()
root.title("IB Style Exam Seating Chart")
root.geometry("500x250")

style = Style(theme="darkly")
style.master = root

global A, B, C

session_years = [
    "2025 MAY",
    "2025 NOV",
    "2026 MAY",
    "2026 NOV",
]
all_subjects = [
    "ENGLISH A Language and Literature",
    "ENGLISH A: Literature",
    "WORLD LANGUAGES A",
    "WORLD LANGUAGES B",
    "BUSINESS MANAGEMENT",
    "ECONOMICS",
    "GEOGRAPHY",
    "GLOBAL POLITICS",
    "HISTORY",
    "PSYCHOLOGY",
    "MATHEMATICS: ANALYSIS AND APPROACHES",
    "MATHEMATICS: APPLICATIONS AND INTERPRETATION",
    "BIOLOGY",
    "CHEMISTRY",
    "PHYSICS",
    "COMPUTER SCIENCE",
    "DESIGN TECHNOLOGY",
    "ENVIRONMENTAL SYSTEMS AND SOCIETIES",
    "SPORTS EX SCI"
]

import sqlite3

def initialize_database():
    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_report (
        subject TEXT NOT NULL,
        Level TEXT NOT NULL,
        session TEXT NOT NULL,
        Session_number TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_info (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        paper TEXT NOT NULL,
        level TEXT NOT NULL,
        length INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS special_students (
        session_number TEXT PRIMARY KEY,
        extra_percent REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Inserting CSV file to Database
def selectfile():
    file_path = filedialog.askopenfilename()
    try:
        print("File path: " + file_path)
        df = pd.read_csv(
            file_path,
            usecols=['Subject', 'Level', 'Session', 'Session number', 'First name', 'Last name']
        )

        conn = sqlite3.connect('seating_chart.db')
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                '''
                INSERT INTO subject_report
                (subject, Level, session, Session_number, first_name, last_name)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    row['Subject'],
                    row['Level'],
                    row['Session'],
                    row['Session number'],
                    row['First name'],
                    row['Last name']
                )
            )

        conn.commit()
        conn.close()

        print("Import CSV file successfully")
        messagebox.showinfo("Import CSV file successfully", "Import CSV file successfully")
    except FileNotFoundError:
        print("file not found")
        messagebox.showerror("File not found", "File not found")
    except Exception as e:
        print("Unexpected Error: ", e)
        messagebox.showerror(
            "Unexpected Error",
            "Error while importing csv file, please check your file and reimport"
        )


def selectsubjects():
    subject_window = ttk.Toplevel(root)
    subject_window.title("Select Subjects")

    text_session = tk.StringVar()
    text_maxstudents = tk.StringVar()
    text_s1 = tk.StringVar()
    text_s2 = tk.StringVar()
    text_s3 = tk.StringVar()

    max_students1 = ttk.Label(subject_window, text="Select Max Students")
    max_students1.grid(row=1, column=2, padx=10, pady=10)

    max_students2 = ttk.Combobox(
        subject_window,
        values=["110", "120", "150"],
        textvariable=text_maxstudents
    )
    max_students2.grid(row=2, column=2, padx=10, pady=10)

    session1 = ttk.Label(subject_window, text='Session')
    session1.grid(row=1, column=1, padx=10, pady=5)

    session2 = ttk.Combobox(
        subject_window,
        values=session_years,
        textvariable=text_session
    )
    session2.grid(row=2, column=1, padx=10, pady=5)

    subject_selection1 = ttk.Label(subject_window, text='Select Subject 1')
    subject_selection1.grid(row=1, column=3, padx=10, pady=5)

    subject_selection2 = ttk.Combobox(
        subject_window,
        values=getExamInfo(),
        textvariable=text_s1,
        width=25
    )
    subject_selection2.grid(row=2, column=3, padx=20, pady=5)

    subject_selection3 = ttk.Label(subject_window, text='Select Subject 2')
    subject_selection3.grid(row=1, column=4, padx=10, pady=5)

    subject_selection4 = ttk.Combobox(
        subject_window,
        values=getExamInfo(),
        textvariable=text_s2,
        width=25
    )
    subject_selection4.grid(row=2, column=4, padx=10, pady=5)

    subject_selection5 = ttk.Label(subject_window, text='Select Subject 3')
    subject_selection5.grid(row=1, column=5, padx=10, pady=5)

    subject_selection6 = ttk.Combobox(
        subject_window,
        values=getExamInfo(),
        textvariable=text_s3,
        width=25
    )
    subject_selection6.grid(row=2, column=5, padx=10, pady=5)

    createsheet = ttk.Button(
        subject_window,
        text="CREATE CHART",
        width=15,
        bootstyle="danger",
        command=lambda: getStudents(text_session, text_maxstudents, text_s1, text_s2, text_s3)
    )
    createsheet.grid(row=3, column=5, padx=10, pady=5, ipady=8)


def subjectlength():
    text_subjectname = tk.StringVar()
    text_paper = tk.StringVar()
    text_level = tk.StringVar()
    text_length = tk.StringVar()

    subjectlength_window = ttk.Toplevel(root)
    subjectlength_window.title("Add Subject Length")

    subjects_label = ttk.Label(subjectlength_window, text="Select 1 subject")
    subjects_label.grid(row=1, column=1, padx=10, pady=10)

    subjects = ttk.Combobox(subjectlength_window, values=all_subjects, textvariable=text_subjectname)
    subjects.grid(row=2, column=1, padx=10, pady=10)

    papersubjects_label = ttk.Label(subjectlength_window, text="Select Paper")
    papersubjects_label.grid(row=1, column=2, padx=10, pady=10)

    papersubjects = ttk.Combobox(
        subjectlength_window,
        values=["Paper 1", "Paper 2", "Paper 3"],
        textvariable=text_paper
    )
    papersubjects.grid(row=2, column=2, padx=10, pady=10)

    levelsubjects_label = ttk.Label(subjectlength_window, text="Select Level")
    levelsubjects_label.grid(row=1, column=3, padx=10, pady=10)

    levelsubjects = ttk.Combobox(
        subjectlength_window,
        values=["SL", "HL"],
        textvariable=text_level
    )
    levelsubjects.grid(row=2, column=3, padx=10, pady=10)

    lengthsubjects_label = ttk.Label(subjectlength_window, text="Enter Length of Exam (In Minutes)")
    lengthsubjects_label.grid(row=1, column=4, padx=10, pady=10)

    lengthsubjects = ttk.Entry(subjectlength_window, textvariable=text_length)
    lengthsubjects.grid(row=2, column=4, padx=10, pady=10)

    submit_button = ttk.Button(
        subjectlength_window,
        text="Submit",
        width=12,
        bootstyle="success",
        command=lambda: examlength_submit(
            text_subjectname, text_paper, text_level, text_length, subjectlength_window
        )
    )
    submit_button.grid(row=3, column=4, padx=10, pady=10, ipady=8)


def examlength_submit(name, paper, level, length, window):
    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO subject_info (subject, paper, level, length) VALUES (?,?,?,?)',
            (name.get(), paper.get(), level.get(), length.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.Error as e:
        messagebox.showinfo("Error", f"An error occurred: {e}")

    conn.close()
    window.destroy()


def getExamInfo():
    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    cursor.execute("select * from subject_info")
    record = cursor.fetchall()
    output = []
    for r in record:
        output.append(r[1] + " " + r[2] + " " + r[3])

    conn.commit()
    conn.close()
    return output


def get_special_students_map():
    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    cursor.execute("select session_number, extra_percent from special_students")
    rows = cursor.fetchall()

    conn.close()
    return {str(row[0]): float(row[1]) for row in rows}


def get_exam_length(cursor, subject, paper, level):
    cursor.execute(
        "select length from subject_info where subject=? and paper=? and level=?",
        (subject, paper, level)
    )
    result = cursor.fetchone()
    if result is None:
        return None
    return int(result[0])


def fetch_subject_records(cursor, session_str, subject, level):
    sql = (
        "select Session_number, first_name, last_name from subject_report "
        "where session=? and subject=? and Level=?"
    )
    cursor.execute(sql, (session_str, subject, level))
    return cursor.fetchall()


def split_main_and_special_students(records, extra_map, exam_length):
    main_students = []
    special_students = []

    for session_number, first_name, last_name in records:
        session_number_str = str(session_number)
        last_three_digits = session_number_str[-3:]
        main_text = last_three_digits + "-" + first_name

        if session_number_str in extra_map:
            extra_percent = float(extra_map[session_number_str])
            adjusted_time = None
            if exam_length is not None:
                adjusted_time = int(round(exam_length * (1 + extra_percent / 100)))

            special_students.append({
                "session_number": session_number_str,
                "seat_id": last_three_digits,
                "name": f"{first_name} {last_name}",
                "time": adjusted_time
            })
        else:
            main_students.append(main_text)

    return main_students, special_students


def removeDuplicates(record1, record2):
    record1_set = set(record1)
    record2_filtered = [item for item in record2 if item not in record1_set]
    return record2_filtered


def split_string(input_string):
    pattern = r"(.+?) (Paper \d) (HL|SL)"
    match = re.match(pattern, input_string)

    if match:
        return match.groups()
    else:
        return None


def getStudents(session, maxStudent, subject1, subject2, subject3):
    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    session_str = session.get()
    record1 = []
    record2 = []
    record3 = []
    special_record1 = []
    special_record2 = []
    special_record3 = []
    extra_map = get_special_students_map()

    subject1_main = subject1.get()
    if len(subject1_main) > 0:
        result = split_string(subject1_main)
        if result:
            subject1_str, paper, level1 = result
            exam_length = get_exam_length(cursor, subject1_str, paper, level1)
            records = fetch_subject_records(cursor, session_str, subject1_str, level1)
            regular, special = split_main_and_special_students(records, extra_map, exam_length)
            record1.extend(regular)
            special_record1.extend(special)

            print(record1)

    subject2_main = subject2.get()
    if len(subject2_main) > 0:
        result = split_string(subject2_main)
        if result:
            subject2_str, paper, level2 = result
            exam_length = get_exam_length(cursor, subject2_str, paper, level2)
            records = fetch_subject_records(cursor, session_str, subject2_str, level2)
            regular, special = split_main_and_special_students(records, extra_map, exam_length)
            record2.extend(regular)
            special_record2.extend(special)

            record2 = removeDuplicates(record1, record2)
            special_record2 = remove_special_duplicates(special_record1, special_record2)

    print(record2)

    subject3_main = subject3.get()
    if len(subject3_main) > 0:
        result = split_string(subject3_main)
        if result:
            subject3_str, paper, level3 = result
            exam_length = get_exam_length(cursor, subject3_str, paper, level3)
            records = fetch_subject_records(cursor, session_str, subject3_str, level3)
            regular, special = split_main_and_special_students(records, extra_map, exam_length)
            record3.extend(regular)
            special_record3.extend(special)

            record3 = removeDuplicates(record2, record3)
            combined_special = special_record1 + special_record2
            special_record3 = remove_special_duplicates(combined_special, special_record3)
            print(record3)

    conn.close()
    colorSeat(record1, record2, record3, maxStudent)

    all_special = special_record1 + special_record2 + special_record3
    if all_special:
        specialSeat(all_special, special_record1, special_record2, special_record3)


def fill_seats(list_data, start_col, num_rows, D, max_cols=10):
    index = 0
    for col in range(start_col, max_cols):
        if col % 2 == start_col % 2:
            for row in range(num_rows):
                if index < len(list_data):
                    D[row][col] = list_data[index]
                    index += 1
                else:
                    return col + 1
        else:
            for row in range(num_rows - 1, -1, -1):
                if index < len(list_data):
                    D[row][col] = list_data[index]
                    index += 1
                else:
                    return col + 1
    return max_cols


def calculate_start_col(previous_list, num_rows, previous_start_col):
    previous_cols = len(previous_list) // num_rows
    if len(previous_list) % num_rows != 0:
        previous_cols += 1
    return previous_start_col + previous_cols


def get_special_seat_text(seat):
    adjusted_time = "N/A" if seat["time"] is None else str(seat["time"])
    return f'{seat["seat_id"]}-{seat["name"]}\n{adjusted_time}'


def display_seats(root, seats, A, B, C, header_labels, seat_text_formatter=str):

    for col_index, label in enumerate(header_labels):
        button = ttk.Button(root, text=label, width=10, bootstyle="secondary")
        button.grid(row=0, column=col_index, padx=5, pady=5)

    for row_index, row in enumerate(seats):
        row_number_button = ttk.Button(
            root,
            text=f"{row_index + 1}",
            width=10,
            bootstyle="secondary"
        )
        row_number_button.grid(row=row_index + 1, column=0, padx=5, pady=5)

        for col_index, seat in enumerate(row):
            if seat is not None:
                if seat in A:
                    button_style = "success"
                elif seat in B:
                    button_style = "warning"
                elif seat in C:
                    button_style = "primary"
                else:
                    button_style = "secondary"

                button = ttk.Button(
                    root,
                    text=seat_text_formatter(seat),
                    width=10,
                    bootstyle=button_style
                )
                button.grid(row=row_index + 1, column=col_index + 1, padx=5, pady=5)


def colorSeat(subject1, subject2, subject3, seatMax):
    print("Seat Arrangement")
    seat_window = ttk.Toplevel(root)
    seat_window.title("Seat Layout")
    seat_window.geometry("1000x1300")

    A = []
    B = []
    C = []

    max_value = int(seatMax.get())
    num_rows = max_value // 10
    D = [[None for _ in range(10)] for _ in range(num_rows)]

    if len(subject2) == 0 and len(subject3) == 0:
        A = subject1
    elif len(subject3) == 0:
        A = subject1
        B = subject2
    else:
        A = subject1
        B = subject2
        C = subject3

    fill_seats(A, 0, num_rows, D, max_cols=10)

    if B:
        next_col_B = calculate_start_col(A, num_rows, 0)
        fill_seats(B, next_col_B, num_rows, D, max_cols=10)

    if C:
        next_col_B = calculate_start_col(A, num_rows, 0)
        next_col_C = calculate_start_col(B, num_rows, next_col_B)
        fill_seats(C, next_col_C, num_rows, D, max_cols=10)
    header_labels = ["#", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    display_seats(seat_window, D, A, B, C, header_labels)


def remove_special_duplicates(previous_records, current_records):
    previous_session_ids = {record["session_number"] for record in previous_records}
    return [record for record in current_records if record["session_number"] not in previous_session_ids]


def specialSeat(special_students, special1, special2, special3):
    special_window = ttk.Toplevel(root)
    special_window.title("Special Room Layout")
    special_window.geometry("700x750")

    special_rows = 5
    special_cols = 5
    room_capacity = special_rows * special_cols

    if len(special_students) > room_capacity:
        messagebox.showwarning(
            "Special Room Capacity Reached",
            "More than 25 students require accommodations. "
            "Only the first 25 are shown in the special room chart."
        )
        special_students = special_students[:room_capacity]

    D = [[None for _ in range(special_cols)] for _ in range(special_rows)]
    fill_seats(special_students, 0, special_rows, D, max_cols=special_cols)

    header_labels = ["#", "A", "B", "C", "D", "E"]
    display_seats(
        special_window,
        D,
        special1,
        special2,
        special3,
        header_labels,
        seat_text_formatter=get_special_seat_text
    )


def add_special_student(session_number_var, extra_time_var, listbox):
    session_number = session_number_var.get().strip()
    extra_percent_text = extra_time_var.get().strip()

    if not session_number or not extra_percent_text:
        messagebox.showerror("Input Error", "Please enter both student session number and extra-time percentage.")
        return

    try:
        extra_percent = float(extra_percent_text)
        if extra_percent < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Extra-time percentage must be a number greater than or equal to 0.")
        return

    conn = sqlite3.connect('seating_chart.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO special_students (session_number, extra_percent) VALUES (?, ?)",
            (session_number, extra_percent)
        )
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        conn.close()
        return

    conn.close()
    refresh_special_students_list(listbox)
    session_number_var.set("")
    extra_time_var.set("")
    messagebox.showinfo("Saved", "Special student saved successfully.")


def refresh_special_students_list(listbox):
    listbox.delete(0, tk.END)
    special_map = get_special_students_map()
    for session_number, extra_percent in special_map.items():
        listbox.insert(tk.END, f"{session_number} - {extra_percent:g}%")


def open_special_students():
    special_window = ttk.Toplevel(root)
    special_window.title("Special Students")
    special_window.geometry("500x420")

    session_number_var = tk.StringVar()
    extra_time_var = tk.StringVar()

    session_label = ttk.Label(special_window, text="Student Session Number")
    session_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ttk.Entry(special_window, textvariable=session_number_var, width=30).grid(
        row=2, column=1, padx=10, pady=5, sticky="w"
    )

    extra_label = ttk.Label(special_window, text="Extra Time (%)")
    extra_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    ttk.Entry(special_window, textvariable=extra_time_var, width=30).grid(
        row=4, column=1, padx=10, pady=5, sticky="w"
    )

    students_label = ttk.Label(special_window, text="Registered Special Students")
    students_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    students_list = tk.Listbox(special_window, width=45, height=10)
    students_list.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    save_button = ttk.Button(
        special_window,
        text="Save Special Student",
        width=20,
        bootstyle="warning",
        command=lambda: add_special_student(session_number_var, extra_time_var, students_list)
    )
    save_button.grid(row=7, column=1, padx=10, pady=12, sticky="w")

    refresh_special_students_list(students_list)


importcvs = ttk.Button(
    root,
    text='Import CSV File',
    command=selectfile,
    width=20,
    bootstyle="primary"
)
importcvs.grid(row=1, column=1, padx=10, pady=10, ipady=10)

addlength = ttk.Button(
    root,
    text='Add Length of exams',
    command=subjectlength,
    width=20,
    bootstyle="success"
)
addlength.grid(row=1, column=2, padx=10, pady=10, ipady=10)

createseating = ttk.Button(
    root,
    text='Start Creating charts',
    command=selectsubjects,
    width=20,
    bootstyle="danger"
)
createseating.grid(row=2, column=1, padx=10, pady=10, ipady=10)

specialstudents = ttk.Button(
    root,
    text='Special Students',
    command=open_special_students,
    width=20,
    bootstyle="warning"
)
specialstudents.grid(row=2, column=2, padx=10, pady=10, ipady=10)


initialize_database()
root.mainloop()
