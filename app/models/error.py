from pydantic import BaseModel
from app.models.types import JSON, AcceptedValue

class RawErrorValidation(BaseModel):
    type: str
    loc: tuple[str, str]
    msg: str
    input: AcceptedValue | JSON

class FormattedErrorValidation(BaseModel):
    field: str
    message: str
    error_type: str
    invalid_value: AcceptedValue | JSON
