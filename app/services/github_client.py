from cachetools import TTLCache
import httpx
from typing import Dict, Any
from app.core.config import GITHUB_TOKEN

GITHUB_API_URL = "https://api.github.com"

# max 100 items & expired after 300s
repo_cache: TTLCache[str, list[Dict[str, Any]]] = TTLCache(maxsize=100, ttl=300)

async def get_repo_details(username: str, repo: str):
    if (cache := repo_cache.get(f"repos/{username}/{repo}")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json() if response.status_code == 200 else None
        if data:
            repo_cache[f"repos/{username}/{repo}"] = data
        return data

async def get_user_details(username: str):
    if (cache := repo_cache.get(f"{username}/details")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json() if response.status_code == 200 else None
        if data:
            repo_cache[f"{username}/details"] = data
        return data

async def get_user_repos(username: str) -> list[Dict[str, Any]]:
    if (cache := repo_cache.get(f"{username}/repos")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            repo_cache[f"{username}/repos"] = response.json()
            return response.json()
        return []
    
async def get_user_followers(username: str) -> list[Dict[str, Any]]:
    if (cache := repo_cache.get(f"{username}/followers")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/users/{username}/followers"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            repo_cache[f"{username}/followers"] = response.json()
            return response.json()
        return []

async def get_search_users(q: str, p: int = 1, limit: int = 5) -> list[Dict[str, Any]]:
    if (cache := repo_cache.get(f"search-user/{q}&page={p}&per_page={limit}")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/search/users?q={q}+in%3Alogin+type%3Auser&page={p}&per_page={limit}&type=users"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            repo_cache[f"search-user/{q}&page={p}&per_page={limit}"] = data
            return data
        return []

async def get_search_repos(q: str, p: int = 1, limit: int = 5) -> list[Dict[str, Any]]:
    if (cache := repo_cache.get(f"search-repos/{q}&page={p}&per_page={limit}")):
        return cache
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}/search/repositories?q={q}&page={p}&per_page={limit}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            repo_cache[f"search-repos/{q}&page={p}&per_page={limit}"] = data
            return data
        return []
