import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Redis settings
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Ollama settings
    OLLAMA_URL = os.getenv("OLLAMA_URL")
    EVALUATION_MODEL_NAME = os.getenv("EVALUATION_MODEL_NAME")
    PROPOSAL_MODEL_NAME = os.getenv("PROPOSAL_MODEL_NAME")

    # Google Sheets settings
    SHEET_ID = os.getenv("SHEET_ID")
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Slack settings
    SLACK_BOT_OAUTH_TOKEN = os.getenv("SLACK_BOT_OAUTH_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")