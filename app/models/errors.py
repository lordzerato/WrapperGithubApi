from pydantic import BaseModel
from typing import Any

class GithubErrorRequest(BaseModel):
    type: str
    loc: Any
    msg: str
    input: Any

class FormattedErrorRequest(BaseModel):
    field: str
    message: str
    error_type: str
    invalid_value: Any
