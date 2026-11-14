import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import boto3
import pytest
from botocore.config import Config
from botocore.stub import Stubber

from app import summary

BUDGET_S = 5.0  # the book page's time budget: the team's choice


def test_throttling_degrades():
    # Stubber answers at the before-call event, so the SDK's retry loop never runs [S27] [S28]
    with Stubber(summary.BEDROCK) as stub:
        stub.add_client_error(
            "converse",
            service_error_code="ThrottlingException",
            service_message="Too many requests",
            http_status_code=429,
        )
        assert summary.summarize_or_none("A book about rivers.") is None


class SlowModel(BaseHTTPRequestHandler):
    def do_POST(self):
        time.sleep(5)  # longer than the client's read timeout


@pytest.fixture
def slow_endpoint():
    server = ThreadingHTTPServer(("127.0.0.1", 0), SlowModel)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def test_slow_model_degrades_within_budget(slow_endpoint, monkeypatch):
    # A real client, so timeouts, retries and backoff all run [S29]
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        endpoint_url=slow_endpoint,
        aws_access_key_id="stand-in",
        aws_secret_access_key="stand-in",
        config=Config(
            connect_timeout=1,
            read_timeout=1,
            retries={"mode": "standard", "total_max_attempts": 2},
        ),
    )
    monkeypatch.setattr(summary, "BEDROCK", client)
    start = time.monotonic()
    assert summary.summarize_or_none("A book about rivers.") is None
    assert time.monotonic() - start < BUDGET_S


def test_production_client_is_bounded():
    cfg = summary.BEDROCK.meta.config  # attribute names: [check]
    assert cfg.connect_timeout <= 2 and cfg.read_timeout <= 10
    assert cfg.retries["mode"] == "standard" and cfg.retries["total_max_attempts"] <= 3
