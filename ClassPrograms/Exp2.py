import pandas as pd

# Read CSV files
students = pd.read_csv("students.csv")
departments = pd.read_csv("departments.csv")
marks = pd.read_csv("marks.csv")

# Merge students with departments
data = pd.merge(students, departments, on="DepartmentID")

# Merge with marks
report = pd.merge(data, marks, on="StudentID")

print("Student Report")
print(report)

# Save the merged report
report.to_csv("student_report.csv", index=False)

print("\nStudent report saved as student_report.csv")