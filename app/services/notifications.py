import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app import app


SLACK_BOT_TOKEN = app.config['SLACK_BOT_OAUTH_TOKEN']

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

CHANNEL_ID = app.config['SLACK_CHANNEL_ID']

def send_slack_notification(job_title, job_url, job_description, ai_evaluation):
    try:
        print("Slack Channel ID:", CHANNEL_ID)
        # Create a Block Kit message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": job_title,
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<https://www.upwork.com{job_url}|View Job on Upwork>"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_{job_description}_"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*AI Summary:*\n{ai_evaluation['summary']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Relevancy:* {ai_evaluation['relevancy']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Key Points:*\n- " + "\n- ".join([f"{keyPoint.get('point', '')} - {keyPoint.get('reason', '')}" for keyPoint in ai_evaluation['keyPoints']])
                }
            }
        ]
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            # ai_evaulation consists of 3 elements: summary, keyPoints, relevancy
            # if job is highly relevant in text we should use alert emoji and red color
            # if job is medium relevant in text we should use warning emoji and yellow color
            # if job is low relevant in text we should use info emoji and blue color
            # text=f"** {job_title} **\nhttps://www.upwork.com{job_url}\n\n{job_description}\n\nAI Summary: {ai_evaluation['summary']}\n\nRelevancy: {ai_evaluation['relevancy']}\n\nKey Points: {ai_evaluation['keyPoints']}"
            text=f"New Job: {job_title}",
            blocks=blocks
        )
        print(f"Message sent to Slack: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e}")

    return
