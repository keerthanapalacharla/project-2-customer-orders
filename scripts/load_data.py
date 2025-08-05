import pandas as pd
import sqlite3
import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths
csv_file = os.path.join(script_dir, "..", "data", "customer_orders.csv")
db_file = os.path.join(script_dir, "..", "db", "orders.db")

# Resolve to absolute paths
csv_file = os.path.abspath(csv_file)
db_file = os.path.abspath(db_file)

# Read the CSV file
df = pd.read_csv(csv_file)

# Display the first few rows to confirm
print("CSV data preview:")
print(df.head())

# Connect to SQLite database
conn = sqlite3.connect(db_file)

# Write the DataFrame to a new table called 'orders'
df.to_sql("orders", conn, if_exists="replace", index=False)

print(f"\nData loaded successfully into database: {db_file}")

# Close the connection
conn.close()
