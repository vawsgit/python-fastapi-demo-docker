# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stand-in for the Bedrock Runtime Converse endpoint, for fault demonstrations only.

Modes: ok (answers at once), slow (waits --delay seconds first), throttle (HTTP 429 ThrottlingException).
"""

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def make_handler(mode: str, delay: float):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):  # Converse is POST /model/{modelId}/converse
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if mode == "throttle":
                self.send_json(
                    429,
                    {"__type": "ThrottlingException", "message": "Too many requests"},
                    {"x-amzn-ErrorType": "ThrottlingException"},
                )
                return
            if mode == "slow":
                time.sleep(delay)  # the client's read timeout fires before this ends
            self.send_json(
                200,
                {
                    "output": {
                        "message": {
                            "role": "assistant",
                            "content": [{"text": "A stand-in summary."}],
                        }
                    },
                    "stopReason": "end_turn",
                    "usage": {"inputTokens": 20, "outputTokens": 5, "totalTokens": 25},
                    "metrics": {"latencyMs": 1},
                },
            )

        def send_json(self, status, body, headers=None):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            for name, value in (headers or {}).items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ok", "slow", "throttle"], default="ok")
    parser.add_argument("--delay", type=float, default=300.0)
    parser.add_argument("--host", default="127.0.0.1")  # private by default
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    ThreadingHTTPServer(
        (args.host, args.port), make_handler(args.mode, args.delay)
    ).serve_forever()
