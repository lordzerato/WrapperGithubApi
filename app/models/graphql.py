from pydantic import BaseModel
from typing import Dict, Optional

type Variables = Optional[Dict[str, str | int | float | bool | None]]

class PayloadGraphQL(BaseModel):
    query: str
    variables: Variables

class PayloadSearch(BaseModel):
    query: str
    page: str | None = None
    per_page: int = 5
