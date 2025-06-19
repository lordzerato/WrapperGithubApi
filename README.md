# WrapperGithubApi

WrapperGithubApi is a backend service designed to support the **RepEx - GitHub Repositories Explorer** project. The main goal of this API is to act as a wrapper around GitHub's REST API and hide the GitHub token to prevent its exposure to the client or frontend, ensuring a secure way to access GitHub data.

## Purpose

This project serves as a server component for the RepEx project (GitHub Repositories Explorer), which can be found at [RepEx GitHub Repository](https://github.com/lordzerato/GitHub-repositories-explorer).

## Technologies Used

- **Python**: The primary programming language.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **HTTPX**: An async HTTP client for making requests to the GitHub API.
- **python-dotenv**: A library to load environment variables from a `.env` file, ensuring that sensitive data (like GitHub tokens) remains secure.
- **Uvicorn**: An ASGI server to run the FastAPI application.
- **Cachetools**: A caching library used to store frequently requested data to optimize performance and reduce load on the GitHub API.

## Available Endpoints

Currently, the following endpoints are available:

- `/repos`: Fetches repository information from GitHub.
- `/user`: Fetches user information from GitHub.

Both of these endpoints interact with the GitHub REST API and return the relevant data.

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

### `/repos`
- Fetch GitHub repository data.

### `/user`
- Fetch GitHub user data.

## Usage Example

Once the server is up and running, you can access the available endpoints:

- Get repository data: `GET /repos`
- Get user data: `GET /user`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project is part of **RepEx - GitHub Repositories Explorer**. Check out the main repository for more information.
