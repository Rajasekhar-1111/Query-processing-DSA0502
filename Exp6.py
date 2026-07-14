import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create Student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    StudentID INTEGER PRIMARY KEY,
    Name TEXT
)
""")

# Create Course table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
    CourseID INTEGER PRIMARY KEY,
    CourseName TEXT
)
""")

# Create Marks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Marks (
    StudentID INTEGER,
    CourseID INTEGER,
    Marks INTEGER,
    FOREIGN KEY(StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY(CourseID) REFERENCES Course(CourseID)
)
""")

# Delete old data
cursor.execute("DELETE FROM Student")
cursor.execute("DELETE FROM Course")
cursor.execute("DELETE FROM Marks")

# Insert Student records
students = [
    (101, "Ravi"),
    (102, "Priya"),
    (103, "Amit")
]
cursor.executemany("INSERT INTO Student VALUES (?, ?)", students)

# Insert Course records
courses = [
    (1, "Python"),
    (2, "Java"),
    (3, "DBMS")
]
cursor.executemany("INSERT INTO Course VALUES (?, ?)", courses)

# Insert Marks records
marks = [
    (101, 1, 85),
    (101, 2, 80),
    (102, 2, 90),
    (103, 3, 75)
]
cursor.executemany("INSERT INTO Marks VALUES (?, ?, ?)", marks)

conn.commit()

# SQL JOIN Query
query = """
SELECT Student.StudentID,
       Student.Name,
       Course.CourseName,
       Marks.Marks
FROM Student
JOIN Marks ON Student.StudentID = Marks.StudentID
JOIN Course ON Course.CourseID = Marks.CourseID
"""

report = pd.read_sql_query(query, conn)

print("Student Course Report")
print(report)

# Save report
report.to_csv("student_course_report.csv", index=False)

print("\nReport saved as student_course_report.csv")

conn.close()