import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_OAUTH_TOKEN")

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

def send_slack_notification(job_title, job_url, job_description, ai_evaluation):
    try:
        print("Slack Channel ID:", CHANNEL_ID)
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            # ai_evaulation consists of 3 elements: summary, keyPoints, relevancy
            # if job is highly relevant in text we should use alert emoji and red color
            # if job is medium relevant in text we should use warning emoji and yellow color
            # if job is low relevant in text we should use info emoji and blue color
            text=f"**{job_title}**\n{job_url}\n\n{job_description}\n\n{ai_evaluation['summary']}\n\nRelevancy: {ai_evaluation['relevancy']}\n\nKey Points: {ai_evaluation['keyPoints']}"
        )
        print(f"Message sent to Slack: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e}")

    return
