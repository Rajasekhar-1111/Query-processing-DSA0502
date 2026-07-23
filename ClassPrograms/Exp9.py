import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="payroll_db",
    user="postgres",
    password="raju4216",
    port="5432"
)

cursor = conn.cursor()

# Drop table if it already exists
cursor.execute("DROP TABLE IF EXISTS Employee")

# Create table
cursor.execute("""
CREATE TABLE Employee (
    EmpID INT PRIMARY KEY,
    Name VARCHAR(50),
    Department VARCHAR(50),
    Basic INT,
    HRA INT,
    DA INT,
    Deduction INT
)
""")

# Insert records
employees = [
    (1, "Ravi", "HR", 30000, 5000, 3000, 2000),
    (2, "Priya", "IT", 40000, 6000, 4000, 2500),
    (3, "Amit", "Finance", 35000, 5500, 3500, 1800),
    (4, "Sneha", "IT", 45000, 7000, 4500, 3000),
    (5, "Kiran", "HR", 28000, 4500, 2500, 1500)
]

cursor.executemany(
    "INSERT INTO Employee VALUES (%s,%s,%s,%s,%s,%s,%s)",
    employees
)

conn.commit()

# Read data
cursor.execute("SELECT * FROM Employee")
rows = cursor.fetchall()

# Create DataFrame with correct column names
df = pd.DataFrame(rows, columns=[
    "EmpID",
    "Name",
    "Department",
    "Basic",
    "HRA",
    "DA",
    "Deduction"
])

# Calculate Net Salary
df["NetSalary"] = df["Basic"] + df["HRA"] + df["DA"] - df["Deduction"]

print("Employee Payroll Data")
print(df)

# Employee with Highest Salary
highest = df[df["NetSalary"] == df["NetSalary"].max()]

print("\nEmployee with Highest Salary")
print(highest)

# Department-wise Salary Summary
summary = df.groupby("Department")["NetSalary"].sum()

print("\nDepartment-wise Salary Summary")
print(summary)

# Export report
df.to_csv("payroll_report.csv", index=False)

print("\nPayroll report saved as payroll_report.csv")

cursor.close()
conn.close()