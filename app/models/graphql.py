from pydantic import BaseModel
from .types import JSON, GraphQLVariables

class PayloadGraphQL(BaseModel):
    query: str
    variables: GraphQLVariables

class PayloadSearch(BaseModel):
    query: str
    page: str | None = None
    per_page: int = 5

class SearchUsers(BaseModel):
    login: str
    name: str | None
    avatarUrl: str
    bio: str | None
    company: str | None
    location: str | None
    url: str

class PageInfo(BaseModel):
    hasNextPage: bool
    endCursor: str | None

class Edge(BaseModel):
    node: SearchUsers

class DataSearch(BaseModel):
    userCount: int
    pageInfo: PageInfo
    edges: list[Edge]

class Data(BaseModel):
    search: DataSearch

class GraphQLSearchUsers(BaseModel):
    data: Data

class GraphQLData(BaseModel):
    data: JSON
