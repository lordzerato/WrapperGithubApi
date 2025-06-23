class GitHubAPIError(Exception):
    def __init__(self, message: str = "Unknown Error", status: int = 500):
        self.message = message
        self.status = status
        super().__init__(message)
