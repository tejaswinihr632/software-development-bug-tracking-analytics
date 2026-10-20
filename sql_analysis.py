
import sqlite3
import pandas as pd

# Connect to the existing database
conn = sqlite3.connect("software_analytics.db")

# Query 1: Total number of issues
query1 = """
SELECT COUNT(*) AS total_issues
FROM github_issues;
"""

# Query 2: Open and closed issues
query2 = """
SELECT state, COUNT(*) AS total_issues
FROM github_issues
GROUP BY state;
"""

# Query 3: Issues with bug labels
query3 = """
SELECT COUNT(*) AS total_bug_issues
FROM github_issues
WHERE is_bug = 'Yes';
"""

# Query 4: Issues by label
query4 = """
SELECT labels, COUNT(*) AS total_issues
FROM github_issues
GROUP BY labels
ORDER BY total_issues DESC
LIMIT 10;
"""

# Query 5: Average closure time
query5 = """
SELECT ROUND(AVG(resolution_days), 2)
       AS average_closure_days
FROM github_issues
WHERE state = 'closed'
  AND resolution_days IS NOT NULL;
"""
query6 = """
SELECT
    issue_number,
    title,
    labels,
    created_at,
    ROUND(
        julianday('now') - julianday(created_at),
        1
    ) AS age_days
FROM github_issues
WHERE state = 'open'
ORDER BY age_days DESC
LIMIT 10;
"""
query7 = """
SELECT
    substr(created_at, 1, 7) AS issue_month,
    COUNT(*) AS total_issues
FROM github_issues
GROUP BY substr(created_at, 1, 7)
ORDER BY issue_month;
"""
query8 = """
SELECT
    state,
    COUNT(*) AS bug_count
FROM github_issues
WHERE is_bug = 'Yes'
GROUP BY state;
"""
query9 = """
SELECT
    COUNT(*) AS total_issues,
    SUM(CASE WHEN state = 'closed' THEN 1 ELSE 0 END)
        AS closed_issues,
    ROUND(
        100.0 * SUM(
            CASE WHEN state = 'closed' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS closure_percentage
FROM github_issues;
"""


queries = [
    ("Total issues", query1),
    ("Issues by status", query2),
    ("Bug issues", query3),
    ("Top 10 label groups", query4),
    ("Average closure time", query5),
    ("Oldest open issues", query6),
    ("Issues by month", query7),
    ("Bug status", query8),
    ("Closure percentage", query9),
]


for title, query in queries:
    print(f"\n--- {title} ---")
    print(pd.read_sql_query(query, conn).to_string(index=False))

conn.close()

