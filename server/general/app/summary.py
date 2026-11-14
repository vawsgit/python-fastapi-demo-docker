import logging
import os

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
REGION = os.environ.get("AWS_REGION", "us-west-2")

# Worst case = 2 x (1 + 2) s + one backoff wait under 1 s = under 7 s
BEDROCK = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    config=Config(
        connect_timeout=1,
        read_timeout=2,
        retries={"mode": "standard", "total_max_attempts": 2},
    ),
)

logger = logging.getLogger(__name__)


def summarize(description: str) -> str:
    response = BEDROCK.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": f"Summarize in two sentences: {description}"}],
            }
        ],
        inferenceConfig={"maxTokens": 200},
    )
    if response.get("stopReason") != "end_turn":
        raise ValueError(f"model stopped with {response.get('stopReason')}")
    return response["output"]["message"]["content"][0]["text"]


def summarize_or_none(description: str) -> str | None:
    """The book page renders without its summary when the model call fails."""
    try:
        return summarize(description)
    except (BotoCoreError, ClientError, ValueError) as error:
        logger.warning("summary unavailable: %s", type(error).__name__)
        return None
