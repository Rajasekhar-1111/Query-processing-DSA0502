import pandas as pd

# Read CSV, JSON and XML files
csv_data = pd.read_csv("students.csv")
json_data = pd.read_json("students.json")
xml_data = pd.read_xml("students.xml")

# Combine all data
df = pd.concat([csv_data, json_data, xml_data], ignore_index=True)

print("Combined Data")
print(df)

# Remove duplicate records
df = df.drop_duplicates()

# Remove missing values
df = df.dropna()

print("\nCleaned Data")
print(df)

# Save cleaned data
df.to_csv("final_students.csv", index=False)

print("\nFinal dataset saved as final_students.csv")