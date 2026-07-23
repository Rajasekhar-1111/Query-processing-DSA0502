import pandas as pd

# Read CSV file
df = pd.read_csv("student_marks.csv")

# Statistics
print("Highest Marks:", df["Marks"].max())
print("Lowest Marks:", df["Marks"].min())
print("Average Marks:", df["Marks"].mean())
print("Median Marks:", df["Marks"].median())
print("Standard Deviation:", df["Marks"].std())

# Assign Grades
def grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 75:
        return "B"
    elif mark >= 60:
        return "C"
    else:
        return "D"

df["Grade"] = df["Marks"].apply(grade)

print("\nStudent Grades")
print(df)

# Top-performing students
top_students = df[df["Marks"] == df["Marks"].max()]

print("\nTop Performing Student(s)")
print(top_students)

# Save the result
df.to_csv("student_grades.csv", index=False)

print("\nStudent grades saved as student_grades.csv")