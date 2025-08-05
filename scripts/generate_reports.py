import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(script_dir, "..", "db", "orders.db"))
sql_path = os.path.abspath(os.path.join(script_dir, "sql_queries.sql"))

# Output folder for CSVs
output_dir = os.path.abspath(os.path.join(script_dir, "..", "data", "reports"))
os.makedirs(output_dir, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Read all SQL queries from the file
with open(sql_path, "r") as file:
    sql_script = file.read()

# Split queries using semicolon (except empty ones)
queries = [q.strip() for q in sql_script.split(";") if q.strip()]

# Run each query and display/save results
for i, query in enumerate(queries, start=1):
    print(f"\n--- Report {i} ---")
    try:
        df = pd.read_sql_query(query, conn)
        print(df)

        # Save to CSV
        output_file = os.path.join(output_dir, f"report_{i}.csv")
        df.to_csv(output_file, index=False)
        print(f"Saved to: {output_file}")

        # Generate bar charts for first 2 reports
        if i == 1:  # Report 1: Total Orders per Customer
            plt.figure(figsize=(8, 5))
            plt.bar(df["customer_name"], df["total_orders"], color='skyblue')
            plt.title("Total Orders per Customer")
            plt.xlabel("Customer Name")
            plt.ylabel("Total Orders")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif i == 2:  # Report 2: Total Amount Spent per Customer
            plt.figure(figsize=(8, 5))
            plt.bar(df["customer_name"], df["total_spent"], color='lightgreen')
            plt.title("Total Amount Spent per Customer")
            plt.xlabel("Customer Name")
            plt.ylabel("Total Spent")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"Error running query {i}: {e}")

# Close connection
conn.close()
