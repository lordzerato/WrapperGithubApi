from pydantic import BaseModel
from typing import TypeVar, Callable, Coroutine, Any
from .base import GITHUB_CLIENT
from app.core.cache import use_cachetools_hybrid
from app.utils.utils import builder_cache_key
from app.models.types import JSON, Methods

T = TypeVar("T", bound=BaseModel)
client = GITHUB_CLIENT.client_request

def make_fetcher(
    model_cls: type[T],
    prefix: str,
    with_prefix: bool = True,
) -> Callable[..., Coroutine[Any, Any, T]]:
    """
    Return an async function that fetches data from GitHub and validates the response
    using the given Pydantic model and endpoint prefix.
    """
    @use_cachetools_hybrid(builder_cache_key, model_cls, prefix)
    async def fetcher(
        path: str,
        query: JSON | str = "",
        method: Methods = "GET"
    ) -> T:
        separator = "/" if with_prefix else ""
        endpoint = f"{prefix}{separator}{path}{query if isinstance(query, str) else ''}"
        return await client(endpoint, method, query if isinstance(query, dict) else None)
    return fetcher
