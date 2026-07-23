import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    StudentID INTEGER PRIMARY KEY,
    Name TEXT,
    Department TEXT,
    Marks INTEGER
)
""")

# Clear old records
cursor.execute("DELETE FROM Student")

# Insert records
students = [
    (101, "Ravi", "CSE", 85),
    (102, "Priya", "IT", 90),
    (103, "Amit", "ECE", 75),
    (104, "Sneha", "CSE", 95),
    (105, "Kiran", "EEE", 67)
]

cursor.executemany("INSERT INTO Student VALUES (?, ?, ?, ?)", students)

conn.commit()

# Retrieve all records
print("All Student Records")
all_students = pd.read_sql_query("SELECT * FROM Student", conn)
print(all_students)

# Filter students with Marks > 80
print("\nStudents with Marks > 80")
filtered = pd.read_sql_query("SELECT * FROM Student WHERE Marks > 80", conn)
print(filtered)

# Export filtered data to CSV
filtered.to_csv("student_report.csv", index=False)

print("\nFiltered report saved as student_report.csv")

conn.close()