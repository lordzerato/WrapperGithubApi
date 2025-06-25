from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("AUTH_TOKEN")
GITHUB_API_URL = "https://api.github.com"
