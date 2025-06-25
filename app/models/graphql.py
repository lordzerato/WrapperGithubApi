from pydantic import BaseModel
from typing import Dict, Optional, List

type Variables = Optional[Dict[str, str | int | float | bool | None]]

class PayloadGraphQL(BaseModel):
    query: str
    variables: Variables

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
    edges: List[Edge]

class Data(BaseModel):
    search: DataSearch

class GraphQLSearchUsers(BaseModel):
    data: Data
