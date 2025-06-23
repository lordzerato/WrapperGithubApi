from fastapi import APIRouter, HTTPException
from app.services.github_client import graphql_search_users, graphql_request
from app.models.graphql import PayloadGraphQL, PayloadSearch

router = APIRouter(prefix="/graphql", tags=["graphql"])

@router.post("/query")
async def graphql_query(payload: PayloadGraphQL):
    query = payload.query
    variables = payload.variables

    if not query:
        raise HTTPException(status_code=400, detail="Missing GraphQL query")

    try:
        response = await graphql_request(query, variables)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return response

@router.post("/searchUser")
async def search_user(payload: PayloadSearch):
    query = payload.query
    page = payload.page
    per_page = payload.per_page

    if not query:
        raise HTTPException(status_code=400, detail="Missing username")
    
    try:
        response = await graphql_search_users(query, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return response

    