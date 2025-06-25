from pydantic import BaseModel
from typing import List
from .user import User
from .repository import RepositoryLong

class UserFound(User):
    score: float

class RepositoryFound(RepositoryLong):
    score: float

class SearchUsers(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[UserFound]

class SearchRepositories(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[RepositoryFound]
