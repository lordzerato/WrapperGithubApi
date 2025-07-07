from app.models.response_schema import GraphQLSearchUsersResponse, GraphQLResponse
from .factory import make_fetcher
# return an async function to fetch and validate based on the provided model and prefix

graphql_request = make_fetcher(GraphQLResponse, "graphql", False)
graphql_search_users = make_fetcher(GraphQLSearchUsersResponse, "graphql", False)
