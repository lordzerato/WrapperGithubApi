from pydantic import RootModel
from typing import List
from .user import User, Profile
from .repository import Repository, RepositoryDetails
from .search import SearchUsers, SearchRepositories
from .graphql import GraphQLSearchUsers

class ProfileResponse(Profile):
    pass

class FollowersResponse(RootModel[List[User]]):
    pass

class RepositoriesResponse(RootModel[List[Repository]]):
    pass

class RepositoryDetailsResponse(RepositoryDetails):
    pass

class SearchUsersResponse(SearchUsers):
    pass

class SearchReposResponse(SearchRepositories):
    pass

class GraphQLSearchUsersResponse(GraphQLSearchUsers):
    pass
