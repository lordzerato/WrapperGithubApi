from pydantic import BaseModel
from typing import List
from .user import User

class License(BaseModel):
    key: str
    name: str
    node_id: str
    spdx_id: str
    url: str

class BaseRepository(BaseModel):
    description: str | None
    full_name: str
    html_url: str
    id: int
    name: str

class Repository(BaseRepository):
    stargazers_count: int

class RepositoryPublic(BaseRepository):
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    fork: bool
    forks_url: str
    git_commits_url: str
    git_tags_url: str
    git_refs_url: str
    hooks_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    node_id: str
    notifications_url: str
    owner: User
    private: bool
    pulls_url: str
    releases_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    url: str

class RepositoryLong(Repository):
    allow_forking: bool
    archive_url: str
    archived: bool
    assignees_url: str
    blobs_url: str
    branches_url: str
    clone_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    created_at: str
    default_branch: str
    deployments_url: str
    disabled: bool
    downloads_url: str
    events_url: str
    fork: bool
    forks: int
    forks_count: int
    forks_url: str
    git_commits_url: str
    git_url: str
    git_tags_url: str
    git_refs_url: str
    has_discussions: bool
    has_downloads: bool
    has_issues: bool
    has_pages: bool
    has_projects: bool
    has_wiki: bool
    homepage: str | None
    hooks_url: str
    is_template: bool
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    language: str | None
    languages_url: str
    license: License | None
    merges_url: str
    milestones_url: str
    mirror_url: str | None
    node_id: str
    notifications_url: str
    open_issues: int
    open_issues_count: int
    owner: User
    private: bool
    pulls_url: str
    pushed_at: str
    releases_url: str
    size: int
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    svn_url: str
    tags_url: str
    teams_url: str
    topics: List[str] = []
    trees_url: str
    updated_at: str
    url: str
    visibility: str
    watchers: int
    watchers_count: int
    web_commit_signoff_required: bool

class Permissions(BaseModel):
    admin: bool
    maintain: bool
    push: bool
    triage: bool
    pull: bool

class RepositoryDetails(RepositoryLong):
    parent: RepositoryLong | None
    source: RepositoryLong | None
    network_count: int
    # permissions: Permissions
    temp_clone_token: str | None = None
    subscribers_count: int

class RepositoryActivity(BaseModel):
    activity_type: str
    actor: User
    after: str
    before: str
    id: int
    node_id: str
    ref: str
    timestamp: str

class Integration(BaseModel):
    created_at: str
    description: str
    external_url: str
    events: List[str]
    html_url: str
    id: int
    name: str
    node_id: str
    owner: User
    permissions: Permissions
    slug: str
    updated_at: str
