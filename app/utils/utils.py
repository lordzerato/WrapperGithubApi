import json
import hashlib
from typing import Any
from urllib.parse import urlencode
from app.models.types import JSON

def join_query_params(params: dict[str, str | int | None]) -> str:
    filtered = {k: v for k, v in params.items() if v not in [None, ""]}
    return "?" + urlencode(filtered) if filtered else ""

def get_hash_value(raw: JSON | str) -> str:
    data = raw if isinstance(raw, str) else json.dumps(raw, sort_keys=True)
    hash = hashlib.sha256(data.encode()).hexdigest()
    return f"{hash}"

def builder_cache_key(path: str, query: JSON | str = "", *args: Any) -> str:
    query_hash = f"{get_hash_value(query)}" if query else ""
    separator = "/" if query_hash and path else ""
    return f"{path}{separator}{query_hash}"
