"""
Test Script: Collect PRs from a small sample of repositories for validation.

Calls collect_prs.py with reduced parameters:
- Only first 5 repos from data/raw/repos.json
- Maximum 10 PRs per repository (instead of 100)
- Smaller batch size (10 instead of 50)

Output: data/processed/pull_requests_test.csv

Use this to validate the collection logic before running the full dataset.
Use: python scripts/test_collect_prs.py
"""

import os
from collect_prs import collect_prs

# Test parameters (reduced for quick validation)
TEST_REPOS_LIMIT = 5  # Only first 5 repos
PRS_PER_REPO = 10  # Only 10 PRs per repo
BATCH_SIZE = 10  # Smaller batch for testing

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data/processed", "pull_requests_test.csv")


if __name__ == "__main__":
    print("TEST MODE: Running collection with limited parameters...\n")
    collect_prs(
        repos_limit=TEST_REPOS_LIMIT,
        prs_per_repo=PRS_PER_REPO,
        batch_size=BATCH_SIZE,
        output_file=OUTPUT_FILE,
    )
    print(f"\n✅ Test complete! Results saved to: {OUTPUT_FILE}")
    print("  Safe to open in Excel and validate before running full collection.")
