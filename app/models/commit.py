from pydantic import BaseModel, Field
from .user import User, Organisation, Author
from .repository import Integration, RepositoryLong

class CommitRefference(BaseModel):
    sha: str
    url: str

class Branch(BaseModel):
    commit: CommitRefference
    name: str
    protected: bool

class PullRequest(BaseModel):
    diff_url: str
    html_url: str
    merged_at: str | None
    patch_url: str
    url: str

class Reactions(BaseModel):
    plus_one: int = Field(0, alias="+1")
    minus_one: int = Field(0, alias="-1")
    confused: int
    eyes: int
    heart: int
    hooray: int
    laugh: int
    rocket: int
    total_count: int
    url: str

class ShortCommit(BaseModel):
    author: Author | None
    distinct: bool
    message: str
    sha: str
    url: str

class Commit(BaseModel):
    active_lock_reason: str | None
    assignee: User | None
    assignees: list[User] = []
    author_association: str
    body: str | None
    closed_at: str | None
    comments_url: str
    created_at: str
    draft: bool
    html_url: str
    id: int
    labels: list[str] = []
    locked: bool
    milestone: str | int | None
    node_id: str
    number: int
    title: str
    state: str
    updated_at: str
    url: str
    user: User

class Issue(Commit):
    closed_by: User | None
    comments: int
    events_url: str
    labels_url: str
    performed_via_github_app: Integration | None
    pull_request: PullRequest
    reactions: Reactions
    repository_url: str
    timeline_url: str
    state_reason: str | None

class Payload(BaseModel):
    before: str
    commits: list[ShortCommit] = []
    distinct_size: int
    head: str
    push_id: int
    ref: str
    repository_id: int
    size: int

class BaseRefference(BaseModel):
    label: str
    ref: str
    sha: str
    user: User
    repo: RepositoryLong

class Href(BaseModel):
    href: str

class Links(BaseModel):
    comments: Href
    commits: Href
    html: Href
    issue: Href
    review_comment: Href
    review_comments: Href
    self: Href
    statuses: Href

class Pull(Commit):
    diff_url: str
    patch_url: str
    issue_url: str
    merged_at: None
    merge_commit_sha: str
    requested_reviewers: list[User] = []
    requested_teams: list[Organisation] = []
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    statuses_url: str
    head: BaseRefference
    base: BaseRefference
    links: Links | None = Field(None, alias="_links")
    auto_merge: None

class ReadMe(BaseModel):
    content: str
    download_url: str
    encoding: str
    git_url: str
    html_url: str
    links: dict[str, str] | None = Field(None, alias="_links")
    name: str
    path: str
    sha: str
    size: int
    type: str
    url: str
