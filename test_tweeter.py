import importlib
import json
import os
import sys
import types
import unittest
from unittest.mock import patch

sys.modules.setdefault("dotenv", types.SimpleNamespace(load_dotenv=lambda: None))

tweeter = importlib.import_module("tweeter")


class TweeterBackendTests(unittest.TestCase):
    def test_format_final_tweet_appends_url(self):
        result = tweeter.format_final_tweet("Useful summary || https://example.com/news")

        self.assertEqual(
            result,
            "Useful summary\n\n#news #AI #tips\n\nhttps://example.com/news",
        )

    def test_xquik_backend_posts_expected_payload(self):
        captured = {}

        class Response:
            status = 202

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return False

            def read(self):
                return json.dumps({"writeActionId": "wa_123"}).encode("utf-8")

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["timeout"] = timeout
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["api_key"] = request.get_header("X-api-key")
            return Response()

        env = {
            "XQUIK_API_KEY": "test-key",
            "XQUIK_ACCOUNT": "main-account",
        }
        with patch.dict(os.environ, env, clear=False):
            with patch("urllib.request.urlopen", fake_urlopen):
                result = tweeter.post_with_xquik("Hello from the scheduler")

        self.assertEqual(captured["url"], "https://xquik.com/api/v1/x/tweets")
        self.assertEqual(captured["timeout"], 30)
        self.assertEqual(
            captured["body"],
            {"account": "main-account", "text": "Hello from the scheduler"},
        )
        self.assertEqual(captured["api_key"], "test-key")
        self.assertEqual(
            result,
            {"backend": "xquik", "status": 202, "body": {"writeActionId": "wa_123"}},
        )
        self.assertEqual(
            tweeter.format_post_result(result),
            "Tweet accepted with Xquik. ID: wa_123\n",
        )


if __name__ == "__main__":
    unittest.main()
