from pydantic import BaseModel
from typing import Any
from app.models.graphql import AcceptedValue

class GithubErrorRequest(BaseModel):
    type: str
    loc: Any
    msg: str
    input: AcceptedValue | dict[str, Any]

class FormattedErrorRequest(BaseModel):
    field: str
    message: str
    error_type: str
    invalid_value: AcceptedValue | dict[str, Any]
