import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# --------------------------
# Setup paths
# --------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.abspath(os.path.join(script_dir, "..", "data", "customer_orders.csv"))
db_file = os.path.abspath(os.path.join(script_dir, "..", "db", "orders.db"))
sql_file = os.path.abspath(os.path.join(script_dir, "sql_queries.sql"))
report_dir = os.path.abspath(os.path.join(script_dir, "..", "data", "reports"))
os.makedirs(report_dir, exist_ok=True)

# --------------------------
# Step 1: Load CSV into SQLite
# --------------------------
print("🔄 Loading data into SQLite database...")

df = pd.read_csv(csv_file)
conn = sqlite3.connect(db_file)
df.to_sql("orders", conn, if_exists="replace", index=False)
print("✅ Data loaded into:", db_file)

# --------------------------
# Step 2: Read and run SQL queries
# --------------------------
print("\n📊 Generating reports...")

with open(sql_file, "r") as file:
    sql_script = file.read()

queries = [q.strip() for q in sql_script.split(";") if q.strip()]

for i, query in enumerate(queries, start=1):
    print(f"\n--- Report {i} ---")
    try:
        df_result = pd.read_sql_query(query, conn)
        print(df_result)

        # Save report as CSV
        report_path = os.path.join(report_dir, f"report_{i}.csv")
        df_result.to_csv(report_path, index=False)
        print(f"💾 Saved to: {report_path}")

        # Generate charts for report 1 and 2
        if i == 1:
            plt.figure(figsize=(8, 5))
            plt.bar(df_result["customer_name"], df_result["total_orders"], color='skyblue')
            plt.title("Total Orders per Customer")
            plt.xlabel("Customer Name")
            plt.ylabel("Total Orders")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif i == 2:
            plt.figure(figsize=(8, 5))
            plt.bar(df_result["customer_name"], df_result["total_spent"], color='lightgreen')
            plt.title("Total Amount Spent per Customer")
            plt.xlabel("Customer Name")
            plt.ylabel("Total Spent")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"❌ Error in Report {i}: {e}")

# Close DB connection
conn.close()

print("\n🎉 All done! Reports and visualizations are ready.")
