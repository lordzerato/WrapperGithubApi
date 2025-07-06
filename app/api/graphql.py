from fastapi import APIRouter, HTTPException
from app.services.github_client.graphql import graphql_search_users, graphql_request
from app.models.graphql import PayloadGraphQL, PayloadSearch
from app.models.response_schema import GraphQLSearchUsersResponse, GraphQLResponse

router = APIRouter(prefix="/graphql", tags=["graphql"])

@router.post("/query", response_model=GraphQLResponse)
async def graphql_query(payload: PayloadGraphQL):
    query = payload.query
    variables = payload.variables

    if not query:
        raise HTTPException(status_code=400, detail="Missing GraphQL query")

    return await graphql_request(query, variables)

@router.post("/searchUser", response_model=GraphQLSearchUsersResponse)
async def search_user(payload: PayloadSearch):
    query = payload.query
    page = payload.page
    per_page = payload.per_page

    if not query:
        raise HTTPException(status_code=400, detail="Missing username")

    return await graphql_search_users(query, page, per_page)
