import pandas as pd

# Read CSV file
df = pd.read_csv("student_data.csv")

print("Original Data")
print(df)

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing Marks with average
df["Marks"] = df["Marks"].fillna(df["Marks"].mean())

# Fill missing Email with "Not Available"
df["Email"] = df["Email"].fillna("Not Available")

# Rename column
df.rename(columns={"Marks": "StudentMarks"}, inplace=True)

# Change data type
df["StudentMarks"] = df["StudentMarks"].astype(int)

print("\nCleaned Data")
print(df)

# Save cleaned data
df.to_csv("cleaned_student_data.csv", index=False)

print("\nCleaned dataset saved as cleaned_student_data.csv")