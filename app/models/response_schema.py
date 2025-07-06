from pydantic import RootModel
from .user import User, Profile, Contributors
from .repository import (
    RepositoryDetails,
    RepositoryActivity,
    RepositoryPublic,
    RepositoryLong,
    Topics
)
from .search import SearchUsers, SearchRepositories
from .graphql import GraphQLSearchUsers, GraphQLData
from .commit import Branch, Issue, Pull, ReadMe
from .event import Event

class UsersDetailsResponse(Profile):
    pass

class UsersRepositoriesResponse(RootModel[list[RepositoryLong]]):
    pass

class UsersFollowersResponse(RootModel[list[User]]):
    pass

class UsersStarredResponse(RootModel[list[RepositoryLong]]):
    pass

class UsersPublicEventsResponse(RootModel[list[Event]]):
    pass

class RepositoriesResponse(RootModel[list[RepositoryPublic]]):
    pass

class RepositoryDetailsResponse(RepositoryDetails):
    pass

class RepositoryActivityResponse(RootModel[list[RepositoryActivity]]):
    pass

class RepositoryContributorsResponse(RootModel[list[Contributors]]):
    pass

class RepositoryBranchesResponse(RootModel[list[Branch]]):
    pass

class RepositoryIssuesResponse(RootModel[list[Issue]]):
    pass

class RepositoryPullsResponse(RootModel[list[Pull]]):
    pass

class RepositorySubscribersResponse(RootModel[list[User]]):
    pass

class RepositoryStargazersResponse(RootModel[list[User]]):
    pass

class RepositoryLanguagesResponse(RootModel[dict[str, int]]):
    pass

class RepositoryTopicsResponse(Topics):
    pass

class RepositoryReadmeResponse(ReadMe):
    pass

class SearchUsersResponse(SearchUsers):
    pass

class SearchReposResponse(SearchRepositories):
    pass

class GraphQLSearchUsersResponse(GraphQLSearchUsers):
    pass

class GraphQLResponse(RootModel[GraphQLData]):
    pass
