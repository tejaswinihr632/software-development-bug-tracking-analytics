
import pandas as pd

# 1. Load the raw GitHub data
df = pd.read_csv("github_issues.csv")

# 2. Remove duplicate issue IDs, if any
df = df.drop_duplicates(subset="issue_id")

# 3. Convert date columns into datetime format
date_columns = ["created_at", "updated_at", "closed_at"]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

# 4. Handle missing labels and assignees
df["labels"] = df["labels"].fillna("Unlabeled")
df["assignees"] = df["assignees"].fillna("Unassigned")

# 5. Create a bug classification column
df["is_bug"] = df["labels"].apply(
    lambda labels: "Yes"
    if "bug" in [label.strip().lower()
                 for label in labels.split(",")]
    else "No"
)

# 6. Calculate issue closure time in days
df["resolution_days"] = (
    df["closed_at"] - df["created_at"]
).dt.total_seconds() / 86400

# Open issues should not have a resolution duration
df.loc[df["state"] == "open", "resolution_days"] = pd.NA

# 7. Create a month column for trend analysis
df["created_month"] = (
    df["created_at"].dt.strftime("%Y-%m")
)

# 8. Save the cleaned dataset
df.to_csv("github_issues_cleaned.csv", index=False)

# 9. Display the results
print("Cleaned dataset shape:", df.shape)
print("\nBug classification:")
print(df["is_bug"].value_counts())

print("\nIssue status:")
print(df["state"].value_counts())

print("\nAverage closure time in days:")
print(round(df["resolution_days"].mean(), 2))

print("\nSaved: github_issues_cleaned.csv")
