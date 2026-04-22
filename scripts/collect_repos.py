"""
Script 1: Collect the 200 most popular repositories on GitHub
that have at least 100 PRs (MERGED + CLOSED).

Uses GitHub GraphQL API.
"""

import os
import json
import time
from dotenv import load_dotenv
from github_api import GitHubAPIClient

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Configuration
SEARCH_BATCH = 20
TARGET_REPOS = 200
MIN_PRS = 100

SEARCH_QUERY_STRING = "stars:>1000 sort:stars-desc"

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data/raw", "repos.json")


def collect_repos():
    """Collect popular repositories and filter those with >= MIN_PRS PRs."""
    client = GitHubAPIClient(GITHUB_TOKEN)
    repos = []
    cursor = None
    page = 0

    print(f"Searching for popular repositories (goal: {TARGET_REPOS} with >= {MIN_PRS} PRs)...")

    while len(repos) < TARGET_REPOS:
        page += 1
        result = client.search_repositories(SEARCH_QUERY_STRING, SEARCH_BATCH, cursor)
        search_data = result.get("data", {}).get("search", {})
        nodes = search_data.get("nodes", [])
        page_info = search_data.get("pageInfo", {})

        if not nodes:
            print("  No more results.")
            break

        for node in nodes:
            if node is None:
                continue
            pr_count = node.get("pullRequests", {}).get("totalCount", 0)
            if pr_count >= MIN_PRS:
                repos.append({
                    "nameWithOwner": node["nameWithOwner"],
                    "url": node["url"],
                    "stars": node["stargazerCount"],
                    "primaryLanguage": (node.get("primaryLanguage") or {}).get("name"),
                    "createdAt": node["createdAt"],
                    "prCount": pr_count,
                })

        print(f"  Page {page}: {len(repos)} selected repositories so far.")

        if not page_info.get("hasNextPage"):
            break
        cursor = page_info["endCursor"]
        time.sleep(1)  # respect rate limit

    # Ensure at most TARGET_REPOS
    repos = repos[:TARGET_REPOS]
    print(f"\nTotal repositories selected: {len(repos)}")

    # Save result
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print(f"Result saved to: {OUTPUT_FILE}")
    return repos


if __name__ == "__main__":
    collect_repos()
