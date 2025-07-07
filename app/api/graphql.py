from fastapi import APIRouter, HTTPException
from app.services.github_client.graphql import graphql_search_users, graphql_request
from app.models.types import JSON
from app.models.graphql import PayloadGraphQL, PayloadSearch
from app.models.response_schema import GraphQLSearchUsersResponse, GraphQLResponse

router = APIRouter(prefix="/graphql", tags=["graphql"])

@router.post("/query", response_model=GraphQLResponse)
async def graphql_query(request_body: PayloadGraphQL):
    query = request_body.query
    variables = request_body.variables

    if not query:
        raise HTTPException(status_code=400, detail="Missing GraphQL query")

    payload: JSON = {"query": query, "variables": variables if variables else {}}
    return await graphql_request("", payload, "POST")

@router.post("/searchUser", response_model=GraphQLSearchUsersResponse)
async def search_user(request_body: PayloadSearch):
    username = request_body.query
    page = request_body.page
    per_page = request_body.per_page

    if not username:
        raise HTTPException(status_code=400, detail="Missing username")

    query = "query SearchUsers($login: String!, $first: Int = 5, $after: String = null) { search(type: USER, query: $login, first: $first, after: $after) { userCount pageInfo { hasNextPage endCursor } edges { node { ... on User { login name avatarUrl bio company location url}}}}}"
    variables: JSON = {"login": username, "after": page, "first": per_page}
    payload: JSON = {"query": query, "variables": variables}
    return await graphql_search_users("", payload, "POST")
