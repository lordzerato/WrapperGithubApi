from pydantic import BaseModel
from .user import Actor
from .repository import ShortRepository
from .commit import Payload

class Event(BaseModel):
    id: int
    type: str
    actor: Actor | None
    repo: ShortRepository | None
    payload: Payload | None
    public: bool
    created_at: str