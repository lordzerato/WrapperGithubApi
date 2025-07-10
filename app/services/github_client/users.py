from app.models.response_schema import (
    UsersDetailsResponse,
    UsersRepositoriesResponse,
    UsersFollowersResponse,
    UsersStarredResponse,
    UsersPublicEventsResponse
)
from .factory import make_fetcher

get_user_details = make_fetcher(UsersDetailsResponse, "users")
get_user_repos = make_fetcher(UsersRepositoriesResponse, "users")
get_user_followers = make_fetcher(UsersFollowersResponse, "users")
get_user_starred = make_fetcher(UsersStarredResponse, "users")
get_user_public_event = make_fetcher(UsersPublicEventsResponse, "users")
