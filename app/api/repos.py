from fastapi import APIRouter, HTTPException
from typing import Literal
from app.services.github_client.repos import (
    get_repo_details,
    get_repo_activity,
    get_repo_contributors,
    get_repo_branches,
    get_repo_issues,
    get_repo_pulls,
    get_repo_subscribers,
    get_repo_stargazers,
    get_repo_languages,
    get_public_repositories,
    get_repo_topics,
    get_repo_readme
)
from app.models.response_schema import (
    RepositoriesResponse,
    RepositoryDetailsResponse,
    RepositoryActivityResponse,
    RepositoryContributorsResponse,
    RepositoryBranchesResponse,
    RepositoryIssuesResponse,
    RepositoryPullsResponse,
    RepositorySubscribersResponse,
    RepositoryStargazersResponse,
    RepositoryLanguagesResponse,
    RepositoryTopicsResponse,
    RepositoryReadmeResponse
)
from app.utils.utils import join_query_params

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("itories", response_model=RepositoriesResponse)
async def public_repositories(since: int | None = None):
    query_params: str = join_query_params({"since": since})
    return await get_public_repositories(f"repositories", query_params)

@router.get("/", include_in_schema=False)
async def root():
    raise HTTPException(400, "Missing username parameter")

@router.get("/{username}", include_in_schema=False)
async def root_username():
    raise HTTPException(400, "Missing repository parameter")

@router.get("//{repository}", include_in_schema=False)
async def root_repository():
    raise HTTPException(400, "Missing username parameter")

@router.get("/{username}/{repository}", response_model=RepositoryDetailsResponse)
async def repo_info(username: str, repository: str):
    return await get_repo_details(f"{username}/{repository}")

@router.get("/{username}/{repository}/activity", response_model=RepositoryActivityResponse)
async def repo_activity(
    username: str,
    repository: str,
    direction: Literal["asc", "desc"] = "desc",
    per_page: int = 30,
    before: str | None = None,
    after: str | None = None,
    ref: str | None = None,
    actor: str | None = None,
    time_periode: Literal["day", "week", "month", "quarter", "year"] | None = None,
    activity_type: Literal["push", "force_push", "branch_creation", "branch_deletion", "pr_merge", "merge_queue_merge"] | None = None
):
    query_params: str = join_query_params({
        "direction": direction,
        "per_page": per_page,
        "before": before,
        "after": after,
        "ref": ref,
        "actor": actor,
        "time_periode": time_periode,
        "activity_type": activity_type
    })
    return await get_repo_activity(f"{username}/{repository}/activity", query_params)

@router.get("/{username}/{repository}/contributors", response_model=RepositoryContributorsResponse)
async def repo_contributors(
    username: str,
    repository: str,
    anon: Literal[1, "true"] | None = None,
    per_page: int = 30,
    page: int = 1
):
    query_params: str = join_query_params({
        "anon": anon,
        "per_page": per_page,
        "page": page
    })
    return await get_repo_contributors(f"{username}/{repository}/contributors", query_params)

@router.get("/{username}/{repository}/branches", response_model=RepositoryBranchesResponse)
async def repo_branches(
    username: str,
    repository: str,
    protected: Literal["true", "false"] | None = None,
    per_page: int = 30,
    page: int = 1
):
    query_params: str = join_query_params({
        "protected": protected,
        "per_page": per_page,
        "page": page
    })
    return await get_repo_branches(f"{username}/{repository}/branches", query_params)

@router.get("/{username}/{repository}/issues", response_model=RepositoryIssuesResponse)
async def repo_issues(
    username: str,
    repository: str,
    milestone: str | int | None = None,
    state: Literal["open", "closed", "all"] = "open",
    assignee: str | None = None,
    type: str | None = None,
    creator: str | None = None,
    mentioned: str | None = None,
    labels: str | None = None,
    sort: Literal["created", "updated", "comments"] = "created",
    direction: Literal["asc", "desc"] = "desc",
    since: str | None = None,
    per_page: int = 30,
    page: int = 1
):
    query_params: str = join_query_params({
        "milestone": milestone,
        "state": state,
        "assignee": assignee,
        "type": type,
        "creator": creator,
        "mentioned": mentioned,
        "labels": labels,
        "sort": sort,
        "direction": direction,
        "since": since,
        "per_page": per_page,
        "page": page
    })
    return await get_repo_issues(f"{username}/{repository}/issues", query_params)

@router.get("/{username}/{repository}/pulls", response_model=RepositoryPullsResponse)
async def repo_pulls(
    username: str,
    repository: str,
    state: Literal["open", "closed", "all"] = "open",
    head: str | None = None,
    base: str | None = None,
    sort: Literal["created", "updated", "popularity", "long-running"] = "created",
    direction: Literal["asc", "desc"] = "desc",
    page: int = 1,
    per_page: int = 30
):
    query_params: str = join_query_params({
        "state": state,
        "head": head,
        "base": base,
        "sort": sort,
        "direction": direction,
        "page": page,
        "per_page": per_page
    })
    return await get_repo_pulls(f"{username}/{repository}/pulls", query_params)

@router.get("/{username}/{repository}/subscribers", response_model=RepositorySubscribersResponse)
async def repo_subscribers(
    username: str,
    repository: str,
    page: int = 1,
    per_page: int = 30
):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_repo_subscribers(f"{username}/{repository}/subscribers", query_params)

@router.get("/{username}/{repository}/stargazers", response_model=RepositoryStargazersResponse)
async def repo_stargazers(
    username: str,
    repository: str,
    page: int = 1,
    per_page: int = 30
):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_repo_stargazers(f"{username}/{repository}/stargazers", query_params)

@router.get("/{username}/{repository}/languages", response_model=RepositoryLanguagesResponse)
async def repo_languages( username: str, repository: str):
    return await get_repo_languages(f"{username}/{repository}/languages")

@router.get("/{username}/{repository}/topics", response_model=RepositoryTopicsResponse)
async def repo_topics(
    username: str,
    repository: str,
    page: int = 1,
    per_page: int = 30
):
    query_params = join_query_params({"page": page, "per_page": per_page})
    return await get_repo_topics(f"{username}/{repository}/topics", query_params)

@router.get("/{username}/{repository}/readme", response_model=RepositoryReadmeResponse)
async def repo_readme(username: str, repository: str, ref: str | None = None):
    query_params: str = join_query_params({"ref": ref})
    return await get_repo_readme(f"{username}/{repository}/readme", query_params)
