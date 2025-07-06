import json
import hashlib
from urllib.parse import urlencode
from app.models.types import JSON

def join_query_params(params: dict[str, str | int | None]) -> str:
    filtered = {k: v for k, v in params.items() if v not in [None, ""]}
    return "?" + urlencode(filtered) if filtered else ""

def get_hash_value(raw: JSON) -> str:
    data = json.dumps(raw, sort_keys=True)
    hash = hashlib.sha256(data.encode()).hexdigest()
    return f"{hash}"