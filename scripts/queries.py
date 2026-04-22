"""
GraphQL queries to GitHub API.
"""

SEARCH_REPOS_QUERY = """
query($queryString: String!, $first: Int!, $after: String) {
  search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
    repositoryCount
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        stargazerCount
        primaryLanguage {
          name
        }
        createdAt
        pullRequests(states: [MERGED, CLOSED]) {
          totalCount
        }
      }
    }
  }
}
"""

PR_QUERY = """
query($owner: String!, $name: String!, $first: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: [MERGED, CLOSED], first: $first, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        title
        state
        createdAt
        mergedAt
        closedAt
        bodyText
        additions
        deletions
        changedFiles
        reviews {
          totalCount
        }
        participants {
          totalCount
        }
        comments {
          totalCount
        }
      }
    }
  }
}
"""
