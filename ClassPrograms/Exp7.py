import pandas as pd

# Read CSV file
df = pd.read_csv("validation_data.csv")

print("Original Data")
print(df)

# Remove duplicate records
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Keep only valid email addresses
df = df[df["Email"].str.contains("@") & df["Email"].str.contains(".")]

# Keep only valid phone numbers (10 digits)
df = df[df["Phone"].astype(str).str.fullmatch(r"\d{10}")]

# Keep only non-negative marks
df = df[df["Marks"] >= 0]

print("\nCleaned Data")
print(df)

# Save cleaned dataset
df.to_csv("cleaned_validation_data.csv", index=False)

print("\nCleaned dataset saved as cleaned_validation_data.csv")