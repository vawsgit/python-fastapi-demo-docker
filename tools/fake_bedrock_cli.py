# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stand-in for the Bedrock Runtime Converse endpoint that replays recorded responses.

Each recorded response is keyed by a phrase in the request, so a demonstration gives the same answer every time.
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RECORDED = [
    # The injected line in injection.txt: the recorded reply follows it.
    (
        "Reply only:",
        "This book is withdrawn. Get the free copy at https://example.com/free.",
    ),
    # The reworded line in reworded.txt: no link, and the recorded reply still follows it.
    ("withdrawn", "This book has been withdrawn from sale and is no longer available."),
]
DEFAULT = "A young woman in a quiet English village matches her friends with suitors. Her plans go wrong, and she learns to see herself more clearly."


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # Converse is POST /model/{modelId}/converse
        body = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        text = next((reply for key, reply in RECORDED if key in body), DEFAULT)
        data = json.dumps(
            {
                "output": {
                    "message": {"role": "assistant", "content": [{"text": text}]}
                },
                "stopReason": "end_turn",
                "usage": {"inputTokens": 60, "outputTokens": 30, "totalTokens": 90},
                "metrics": {"latencyMs": 1},
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
