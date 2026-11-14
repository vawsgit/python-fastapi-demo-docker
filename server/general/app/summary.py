import os

import boto3

MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-haiku-20241022-v1:0"
)
REGION = os.environ.get("AWS_REGION", "us-west-2")

BEDROCK = boto3.client("bedrock-runtime", region_name=REGION)


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
    return response["output"]["message"]["content"][0]["text"]
