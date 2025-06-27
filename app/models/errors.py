from pydantic import BaseModel
from typing import Any
from app.models.graphql import AcceptedValue

class RawErrorValidation(BaseModel):
    type: str
    loc: Any
    msg: str
    input: AcceptedValue | dict[str, Any]

class FormattedErrorValidation(BaseModel):
    field: str
    message: str
    error_type: str
    invalid_value: AcceptedValue | dict[str, Any]
