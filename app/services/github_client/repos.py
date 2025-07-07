from app.models.response_schema import (
    RepositoriesResponse,
    RepositoryDetailsResponse,
    RepositoryActivityResponse,
    RepositoryContributorsResponse,
    RepositoryBranchesResponse,
    RepositoryIssuesResponse,
    RepositoryPullsResponse,
    RepositorySubscribersResponse,
    RepositoryStargazersResponse,
    RepositoryLanguagesResponse,
    RepositoryTopicsResponse,
    RepositoryReadmeResponse
)
from .factory import make_fetcher
# return an async function to fetch and validate based on the provided model and prefix

get_public_repositories = make_fetcher(RepositoriesResponse, "repos", False)
get_repo_details = make_fetcher(RepositoryDetailsResponse, "repos")
get_repo_activity = make_fetcher(RepositoryActivityResponse, "repos")
get_repo_contributors = make_fetcher(RepositoryContributorsResponse, "repos")
get_repo_branches = make_fetcher(RepositoryBranchesResponse, "repos")
get_repo_issues = make_fetcher(RepositoryIssuesResponse, "repos")
get_repo_pulls = make_fetcher(RepositoryPullsResponse, "repos")
get_repo_subscribers = make_fetcher(RepositorySubscribersResponse, "repos")
get_repo_stargazers = make_fetcher(RepositoryStargazersResponse, "repos")
get_repo_languages = make_fetcher(RepositoryLanguagesResponse, "repos")
get_repo_topics = make_fetcher(RepositoryTopicsResponse, "repos")
get_repo_readme = make_fetcher(RepositoryReadmeResponse, "repos")
