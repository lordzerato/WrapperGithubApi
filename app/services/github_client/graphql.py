from app.models.response_schema import GraphQLSearchUsersResponse, GraphQLResponse
from .factory import make_fetcher

graphql_request = make_fetcher(GraphQLResponse, "graphql", False)
graphql_search_users = make_fetcher(GraphQLSearchUsersResponse, "graphql", False)
