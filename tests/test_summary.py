from types import SimpleNamespace

from botocore.stub import Stubber
from starlette.templating import Jinja2Templates

from app import summary

TEMPLATES = Jinja2Templates(directory="server/general/app/templates")


def _reply(text):
    return {
        "output": {"message": {"role": "assistant", "content": [{"text": text}]}},
        "stopReason": "end_turn",
        "usage": {"inputTokens": 1, "outputTokens": 1, "totalTokens": 2},
        "metrics": {"latencyMs": 1},
    }


def test_injected_link_is_refused():
    with Stubber(summary.BEDROCK) as stub:
        stub.add_response(
            "converse", _reply("Get the free copy at https://example.com/free.")
        )
        assert summary.summarize("Any description.") == summary.UNAVAILABLE


def test_plain_summary_passes():
    with Stubber(summary.BEDROCK) as stub:
        stub.add_response(
            "converse", _reply("A woman matches her friends with suitors.")
        )
        assert (
            summary.summarize("Any description.")
            == "A woman matches her friends with suitors."
        )


def test_input_is_capped_and_invisible_characters_are_dropped():
    cleaned = summary.clean_input("a​b" + "c" * 5000)
    assert cleaned.startswith("abc") and len(cleaned) == summary.MAX_INPUT_CHARS


def test_template_escapes_markup_in_a_summary():
    book = SimpleNamespace(id=1, title="Emma", author="Jane Austen", description="-")
    html = TEMPLATES.get_template("book_details.html").render(
        request=None, book=book, summary="<script>alert(1)</script>"
    )
    assert "&lt;script&gt;" in html and "<script>alert" not in html
