from fastapi import APIRouter, HTTPException
from typing import Any
from app.services.github_client import graphql_search_users, graphql_request
from app.models.graphql import PayloadGraphQL, PayloadSearch
from app.models.response_schema import GraphQLSearchUsersResponse

router = APIRouter(prefix="/graphql", tags=["graphql"])

@router.post("/query", response_model=dict[str, Any], include_in_schema=False)
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
