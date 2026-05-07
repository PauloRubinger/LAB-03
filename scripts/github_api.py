"""
Reusable client for GitHub GraphQL API.
"""

import time
import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError, Timeout
from queries import SEARCH_REPOS_QUERY, PR_QUERY


class GitHubAPIClient:
    """Client for GitHub GraphQL API."""

    GRAPHQL_URL = "https://api.github.com/graphql"
    MAX_RETRIES = 5
    RETRY_WAIT = 15  # base wait in seconds; doubles each attempt (exponential backoff)

    def __init__(self, token: str):
        """
        Initialize the client.

        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def run_query(self, query: str, variables: dict = None) -> dict:
        """
        Send a GraphQL query to the GitHub API.

        Args:
            query: GraphQL query string
            variables: Query variables dictionary

        Returns:
            Query result as dictionary

        Raises:
            RuntimeError: If fails after MAX_RETRIES attempts
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        for attempt in range(self.MAX_RETRIES):
            try:
                resp = requests.post(
                    self.GRAPHQL_URL,
                    json=payload,
                    headers=self.headers,
                    timeout=60
                )

                if resp.status_code == 200:
                    result = resp.json()
                    if "errors" in result:
                        errors = result["errors"]
                        print(f"  GraphQL errors: {errors}")
                        # Even with errors, return the result
                    return result

                elif resp.status_code == 403:
                    # Rate limit – wait and retry
                    reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
                    wait = max(reset - int(time.time()), 10)
                    print(f"  Rate limit hit. Waiting {wait}s...")
                    time.sleep(wait)

                elif resp.status_code in (502, 503):
                    # Bad Gateway / Service Unavailable – retry with backoff
                    wait = self.RETRY_WAIT * (2 ** attempt)
                    print(f"  HTTP {resp.status_code}. Attempt {attempt + 1}/{self.MAX_RETRIES}. Waiting {wait}s...")
                    time.sleep(wait)

                else:
                    wait = self.RETRY_WAIT * (2 ** attempt)
                    print(f"  HTTP {resp.status_code}: {resp.text}")
                    time.sleep(wait)

            except Timeout:
                # Request timed out – retry with backoff
                wait = self.RETRY_WAIT * (2 ** attempt)
                print(f"  Request timed out. Attempt {attempt + 1}/{self.MAX_RETRIES}. Waiting {wait}s...")
                time.sleep(wait)

            except (ChunkedEncodingError, ConnectionError) as e:
                # Network error – retry with backoff
                wait = self.RETRY_WAIT * (2 ** attempt)
                print(f"  Connection error: {type(e).__name__}. Attempt {attempt + 1}/{self.MAX_RETRIES}. Waiting {wait}s...")
                time.sleep(wait)

        raise RuntimeError(f"Failed after {self.MAX_RETRIES} attempts on GraphQL API.")

    def search_repositories(
        self,
        query_string: str,
        first: int = 20,
        after: str = None
    ) -> dict:
        """
        Search repositories on GitHub API.

        Args:
            query_string: Search query (e.g., "stars:>1000 sort:stars-desc")
            first: Number of results per page
            after: Pagination cursor

        Returns:
            Search result containing repositories
        """
        variables = {
            "queryString": query_string,
            "first": first,
            "after": after,
        }
        return self.run_query(SEARCH_REPOS_QUERY, variables)

    def fetch_pull_requests(
        self,
        owner: str,
        name: str,
        first: int = 50,
        after: str = None
    ) -> dict:
        """
        Fetch pull requests from a repository.

        Args:
            owner: Repository owner
            name: Repository name
            first: Number of PRs per page
            after: Pagination cursor

        Returns:
            Result containing pull requests
        """
        variables = {
            "owner": owner,
            "name": name,
            "first": first,
            "after": after,
        }
        return self.run_query(PR_QUERY, variables)
