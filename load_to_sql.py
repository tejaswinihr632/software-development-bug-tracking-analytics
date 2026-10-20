
import pandas as pd
import sqlite3

# Load the cleaned dataset
df = pd.read_csv("github_issues_cleaned.csv")

# Connect to a SQLite database
conn = sqlite3.connect("software_analytics.db")

# Create a table and load the data
df.to_sql(
    "github_issues",
    conn,
    if_exists="replace",
    index=False
)

print("Data successfully loaded into SQLite!")
print("Rows loaded:", len(df))

# Run our first SQL query
query = """
SELECT state, COUNT(*) AS total_issues
FROM github_issues
GROUP BY state;
"""

result = pd.read_sql_query(query, conn)

print("\nIssues by status:")
print(result)

conn.close()
