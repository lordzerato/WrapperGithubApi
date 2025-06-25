# WrapperGithubApi

WrapperGithubApi is a backend service designed to support the **RepEx - GitHub Repositories Explorer** project. This API acts as a secure wrapper around GitHub's REST and GraphQL APIs, hiding the GitHub token to prevent exposure on the frontend.

## Purpose

This project serves as a secure intermediary layer for GitHub data access in the RepEx project ([GitHub Repository Explorer](https://github.com/lordzerato/GitHub-repositories-explorer)).

## Key Features

- Secure GitHub API access (REST & GraphQL)
- Built with FastAPI + Uvicorn for high performance
- Response time logging via middleware
- OpenAPI and ReDoc auto-generated documentation at `/docs` and `/redoc`
- Centralized error handler for consistent API responses
- Built-in caching using `cachetools`

## Technologies Used

- **Python**: The primary programming language.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **HTTPX**: An async HTTP client for making requests to the GitHub API.
- **python-dotenv**: A library to load environment variables from a `.env` file, ensuring that sensitive data (like GitHub tokens) remains secure.
- **Uvicorn**: An ASGI server to run the FastAPI application.
- **Cachetools**: A caching library used to store frequently requested data to optimize performance and reduce load on the GitHub API.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/WrapperGithubApi.git
    cd WrapperGithubApi
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file in the project root, based on the provided `.env.example`:
    ```env
    AUTH_TOKEN=your_github_token
    ```

4. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `/repos/{user}/{repository}` | Fetch details of a specific GitHub repository. |
| `/user/{user}` | Get public profile info of a GitHub user. |
| `/user/{user}/repos` | Get all public repositories of a GitHub user. |
| `/user/{user}/followers` | List followers of a GitHub user. |
| `/search/users?q={user}&page={page}&per_page={limit}` | Search GitHub users. |
| `/search/repositories?q={query}&page={page}&per_page={limit}` | Search repositories. |
| `/graphql/query` (POST)                                        | Submit GraphQL queries to GitHub's GraphQL API.             |
| `/graphql/searchUser` (POST)                                        | Search Github users with GraphQL API.             |

> Interactive API documentation available at:
> - Swagger UI: [`/docs`](http://localhost:8000/docs)
> - ReDoc: [`/redoc`](http://localhost:8000/redoc)

## Usage Example

Once the server is up and running, you can access the available endpoints:

- Get repository info:
    ```http
    GET /repos/octocat/Hello-World
    ```
- Get user data:
    ```http
    GET /user/octocat
    ```
- Query GraphQL:
    ```http
    POST /graphql/query
    Content-Type: application/json
    
    {
      "query": "{ viewer { login } }"
    }
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project is part of **RepEx - GitHub Repositories Explorer**. Check out the main repository for more information.
