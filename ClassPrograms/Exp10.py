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

# Drop table if it exists
cursor.execute("DROP TABLE IF EXISTS Sales")

# Create Sales table
cursor.execute("""
CREATE TABLE Sales(
    Product VARCHAR(50),
    Quantity INT,
    Price INT,
    Month VARCHAR(20)
)
""")

# Insert January data
cursor.executemany(
    "INSERT INTO Sales VALUES (%s,%s,%s,%s)",
    [
        ("Laptop",10,50000,"January"),
        ("Mobile",20,20000,"January"),
        ("Keyboard",30,1000,"January"),
        ("Mouse",40,500,"January")
    ]
)

# Insert February data
cursor.executemany(
    "INSERT INTO Sales VALUES (%s,%s,%s,%s)",
    [
        ("Laptop",8,50000,"February"),
        ("Mobile",18,20000,"February"),
        ("Keyboard",25,1000,"February"),
        ("Mouse",35,500,"February")
    ]
)

# Insert March data
cursor.executemany(
    "INSERT INTO Sales VALUES (%s,%s,%s,%s)",
    [
        ("Laptop",12,50000,"March"),
        ("Mobile",22,20000,"March"),
        ("Keyboard",28,1000,"March"),
        ("Mouse",38,500,"March")
    ]
)

conn.commit()

# Read data
cursor.execute("SELECT * FROM Sales")
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=[
    "Product",
    "Quantity",
    "Price",
    "Month"
])

# Calculate Sales
df["Sales"] = df["Quantity"] * df["Price"]

print("Sales Data")
print(df)

# Total Sales
print("\nTotal Products Sold:", df["Quantity"].sum())

# Monthly Revenue
print("\nMonthly Revenue")
print(df.groupby("Month")["Sales"].sum())

# Top Selling Product
top = df.groupby("Product")["Quantity"].sum().idxmax()
print("\nTop Selling Product:", top)

# Product Summary
print("\nProduct Summary")
print(df.groupby("Product")[["Quantity","Sales"]].sum())

# Export report
df.to_csv("sales_report.csv", index=False)

print("\nSales report saved as sales_report.csv")

cursor.close()
conn.close()