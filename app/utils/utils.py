from urllib.parse import urlencode

def join_query_params(params: dict[str, str | int | None]) -> str:
    filtered = {k: v for k, v in params.items() if v not in [None, ""]}
    return "?" + urlencode(filtered) if filtered else ""