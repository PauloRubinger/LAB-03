"""
Script 2: Collect Pull Requests and metrics from each selected repository.

For each repository in data/repos.json, collects PRs (MERGED and CLOSED) with:
- At least 1 review
- Analysis time >= 1 hour

Metrics collected per PR:
- Size: changed files, added lines, removed lines
- Analysis time: interval between creation and closing/merge
- Description: number of characters in PR body (markdown)
- Interactions: number of participants, number of comments
- Number of reviews
- Status: MERGED or CLOSED
"""

import os
import json
import time
import csv
from datetime import datetime
from dotenv import load_dotenv
from github_api import GitHubAPIClient

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Default file paths and parameters
DEFAULT_REPOS_FILE = os.path.join(os.path.dirname(__file__), "..", "data/raw", "repos.json")
DEFAULT_OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data/processed", "pull_requests.csv")
DEFAULT_PRS_PER_REPO = 100
DEFAULT_BATCH_SIZE = 50  # maximum per page in GraphQL API


def parse_datetime(dt_str: str) -> datetime:
    if dt_str is None:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def hours_diff(dt1: datetime, dt2: datetime) -> float:
    if dt1 is None or dt2 is None:
        return 0.0
    return (dt2 - dt1).total_seconds() / 3600.0


def collect_prs(
    repos_limit: int = None,
    prs_per_repo: int = DEFAULT_PRS_PER_REPO,
    batch_size: int = DEFAULT_BATCH_SIZE,
    output_file: str = DEFAULT_OUTPUT_CSV,
    repos_file: str = DEFAULT_REPOS_FILE,
):
    """
    Collect PRs from repositories with the necessary metrics.
    
    Args:
        repos_limit: Limit number of repos to process (None = all)
        prs_per_repo: Maximum PRs to collect per repository
        batch_size: Batch size for API requests
        output_file: Output CSV file path
        repos_file: Input repositories JSON file path
    """
    client = GitHubAPIClient(GITHUB_TOKEN)
    
    with open(repos_file, "r", encoding="utf-8") as f:
        repos = json.load(f)

    # Apply repos limit if specified
    if repos_limit is not None:
        repos = repos[:repos_limit]
    
    print(f"Collecting PRs from {len(repos)} repositories...")

    csv_fields = [
        "repo", "pr_number", "title", "state",
        "created_at", "closed_at", "merged_at",
        "analysis_time_hours",
        "changed_files", "additions", "deletions",
        "body_length",
        "review_count", "participants", "comments",
    ]

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()

        total_prs = 0

        for idx, repo in enumerate(repos, 1):
            owner, name = repo["nameWithOwner"].split("/")
            print(f"\n[{idx}/{len(repos)}] {repo['nameWithOwner']}...")

            cursor = None
            repo_count = 0

            while repo_count < prs_per_repo:
                batch = min(batch_size, prs_per_repo - repo_count)

                try:
                    result = client.fetch_pull_requests(owner, name, batch, cursor)
                except RuntimeError as e:
                    print(f"  Error: {e}. Skipping repository.")
                    break

                repo_data = result.get("data", {}).get("repository")
                if not repo_data:
                    print("  Repository not found or no access.")
                    break

                pr_data = repo_data.get("pullRequests", {})
                nodes = pr_data.get("nodes", [])
                page_info = pr_data.get("pageInfo", {})

                if not nodes:
                    break

                for pr in nodes:
                    if pr is None:
                        continue

                    review_count = pr.get("reviews", {}).get("totalCount", 0)
                    if review_count < 1:
                        continue

                    created = parse_datetime(pr.get("createdAt"))
                    merged = parse_datetime(pr.get("mergedAt"))
                    closed = parse_datetime(pr.get("closedAt"))

                    # Last activity: merge or close
                    last_activity = merged or closed
                    analysis_hours = hours_diff(created, last_activity)

                    # Filter: review took at least 1 hour
                    if analysis_hours < 1.0:
                        continue

                    body = pr.get("bodyText") or ""

                    row = {
                        "repo": repo["nameWithOwner"],
                        "pr_number": pr["number"],
                        "title": pr.get("title", ""),
                        "state": pr["state"],
                        "created_at": pr.get("createdAt"),
                        "closed_at": pr.get("closedAt"),
                        "merged_at": pr.get("mergedAt"),
                        "analysis_time_hours": round(analysis_hours, 2),
                        "changed_files": pr.get("changedFiles", 0),
                        "additions": pr.get("additions", 0),
                        "deletions": pr.get("deletions", 0),
                        "body_length": len(body),
                        "review_count": review_count,
                        "participants": pr.get("participants", {}).get("totalCount", 0),
                        "comments": pr.get("comments", {}).get("totalCount", 0),
                    }
                    writer.writerow(row)
                    repo_count += 1
                    total_prs += 1

                if not page_info.get("hasNextPage"):
                    break
                cursor = page_info["endCursor"]
                time.sleep(0.5)

            print(f"  PRs collected: {repo_count}")

    print(f"\nTotal PRs collected: {total_prs}")
    print(f"Dataset saved to: {output_file}")


if __name__ == "__main__":
    collect_prs()
