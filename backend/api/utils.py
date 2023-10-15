from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .settings import settings

CLIENT = WebClient(token=settings.SLACK_TOKEN.get_secret_value())


def slack_send(text: str, channel: str = "#showyourstripes-errors"):
    """Send a slack notification to a given channel.
    See https://slack.dev/python-slack-sdk/installation/"""
    try:
        CLIENT.chat_postMessage(text=text, channel=channel)
    except SlackApiError as e:
        logger.error(f"Got an error: {e}")
