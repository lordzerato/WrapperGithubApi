from pydantic import RootModel
from typing import List, Dict
from .user import User, Profile, Contributors
from .repository import RepositoryDetails, RepositoryActivity, RepositoryPublic, RepositoryLong
from .search import SearchUsers, SearchRepositories
from .graphql import GraphQLSearchUsers
from .commit import Branch, Issue, Pull

class ProfileResponse(Profile):
    pass

class FollowersResponse(RootModel[List[User]]):
    pass

class RepositoriesResponse(RootModel[List[RepositoryPublic]]):
    pass

class UsersRepositoriesResponse(RootModel[List[RepositoryLong]]):
    pass

class RepositoryDetailsResponse(RepositoryDetails):
    pass

class RepositoryActivityResponse(RootModel[List[RepositoryActivity]]):
    pass

class RepositoryContributorsResponse(RootModel[List[Contributors]]):
    pass

class RepositoryBranchesResponse(RootModel[List[Branch]]):
    pass

class RepositoryIssuesResponse(RootModel[List[Issue]]):
    pass

class RepositoryPullsResponse(RootModel[List[Pull]]):
    pass

class RepositorySubscribersResponse(RootModel[List[User]]):
    pass

class RepositoryStargazersResponse(RootModel[List[User]]):
    pass

class RepositoryLanguagesResponse(RootModel[Dict[str, int]]):
    pass

class SearchUsersResponse(SearchUsers):
    pass

class SearchReposResponse(SearchRepositories):
    pass

class GraphQLSearchUsersResponse(GraphQLSearchUsers):
    pass
