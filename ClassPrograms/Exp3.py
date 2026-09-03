import pandas as pd

# Read CSV file
df = pd.read_csv("data.csv")

print("CSV Data")
print(df)

# Convert CSV to JSON
df.to_json("data.json", orient="records", indent=4)

# Convert CSV to XML
df.to_xml("data.xml", index=False)

# Read JSON file
json_data = pd.read_json("data.json")

print("\nJSON Data")
print(json_data)

# Read XML file
xml_data = pd.read_xml("data.xml")

print("\nXML Data")
print(xml_data)

print("\nConversion completed successfully.")