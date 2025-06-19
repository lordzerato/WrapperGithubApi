from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("AUTH_TOKEN")
