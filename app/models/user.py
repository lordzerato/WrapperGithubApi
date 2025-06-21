from pydantic import BaseModel

class User(BaseModel):
    avatar_url: str
    events_url: str
    followers_url: str
    following_url: str
    gists_url: str
    gravatar_id: str
    html_url: str
    id: int
    login: str
    node_id: str
    organizations_url: str
    received_events_url: str
    repos_url: str
    site_admin: bool
    starred_url: str
    subscriptions_url: str
    type: str
    url: str
    user_view_type: str

class Profile(User):
    bio: str | None
    blog: str | None
    company: str | None
    created_at: str
    email: str | None
    followers: int
    following: int
    hireable: bool | None
    location: str | None
    name: str | None
    public_gists: int
    public_repos: int
    twitter_username: str | None
    updated_at: str
