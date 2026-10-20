
import requests
import pandas as pd

# 1. Choose the GitHub repository
owner = "microsoft"
repo = "vscode"

# 2. Build the API URL
url = f"https://api.github.com/repos/microsoft/vscode/issues"

# 3. Request issue data from GitHub
all_issues = []

for page in range(1, 6):
    params = {
        "state": "all",
        "per_page": 100,
        "page": page
    }

    response = requests.get(url, params=params, timeout=30)

    # Stop if GitHub returns an error
    response.raise_for_status()

    issues = response.json()

    if not issues:
        break

    all_issues.extend(issues)

print("Records received:", len(all_issues))

# 4. Remove pull requests
issues_only = [
    issue for issue in all_issues
    if "pull_request" not in issue
]

# 5. Extract useful columns
rows = []

for issue in issues_only:
    rows.append({
        "issue_id": issue["id"],
        "issue_number": issue["number"],
        "title": issue["title"],
        "state": issue["state"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "closed_at": issue["closed_at"],
        "comments": issue["comments"],
        "labels": ", ".join(
            label["name"] for label in issue["labels"]
        ),
        "assignees": ", ".join(
            person["login"] for person in issue["assignees"]
        ),
        "issue_url": issue["html_url"]
    })

# 6. Convert the records into a table
df = pd.DataFrame(rows)

# 7. Save the data as a CSV file
df.to_csv("github_issues.csv", index=False)

print("Issue records saved:", len(df))
print("File created: github_issues.csv")
print(df.head())
