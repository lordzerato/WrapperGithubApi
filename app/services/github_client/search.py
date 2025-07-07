from app.models.response_schema import SearchUsersResponse, SearchReposResponse
from app.services.github_client.factory import make_fetcher
# return an async function to fetch and validate based on the provided model and prefix

get_search_users = make_fetcher(SearchUsersResponse, "search")
get_search_repos = make_fetcher(SearchReposResponse, "search")
