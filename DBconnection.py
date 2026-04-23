import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('seating_chart.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the subject_report table
create_subject_table = '''
CREATE TABLE IF NOT EXISTS subject_report (
    subject TEXT NOT NULL,
    Level TEXT NOT NULL,
    session TEXT NOT NULL,
    Session_number TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);
'''

# Create the subject_report table
create_subjectinfo_table = '''
CREATE TABLE IF NOT EXISTS subject_info (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    paper TEXT NOT NULL,
    level TEXT NOT NULL,
    length INTEGER NOT NULL
);
'''

# Execute the query
cursor.execute(create_subject_table)
cursor.execute(create_subjectinfo_table)

create_special_students_table = '''
CREATE TABLE IF NOT EXISTS special_students (
    session_number TEXT PRIMARY KEY,
    extra_percent REAL NOT NULL
);
'''
cursor.execute(create_special_students_table)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database and table created successfully.")
