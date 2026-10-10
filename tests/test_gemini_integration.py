import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import httpx
from fastapi import HTTPException
from google.genai import errors, types

import main


class GeminiIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = main.DB_PATH
        main.DB_PATH = Path(self.temp_dir.name) / "test.db"
        main.init_db()
        self.generate_content = Mock()
        self.client = SimpleNamespace(
            models=SimpleNamespace(generate_content=self.generate_content)
        )
        self.make_client = patch("main.make_client", return_value=self.client)
        self.make_client.start()

    def tearDown(self) -> None:
        self.make_client.stop()
        main.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_chat_sends_recent_turns_and_returns_usage(self) -> None:
        self.generate_content.return_value = SimpleNamespace(
            text="Hampi is known for its historic monuments.",
            usage_metadata=SimpleNamespace(total_token_count=31),
        )

        first = main.chat(main.ChatRequest(session_id="session-1", message="Tell me about Hampi"))
        second = main.chat(main.ChatRequest(session_id="session-1", message="What about its history?"))

        self.assertEqual(first.tokens_used, 31)
        self.assertIn("historic monuments", first.reply)
        self.assertEqual(second.session_id, "session-1")
        contents = self.generate_content.call_args.kwargs["contents"]
        self.assertEqual([turn.role for turn in contents], ["user", "model", "user"])
        self.assertEqual(
            [turn.parts[0].text for turn in contents],
            [
                "Tell me about Hampi",
                "Hampi is known for its historic monuments.",
                "What about its history?",
            ],
        )
        self.assertIsInstance(
            self.generate_content.call_args.kwargs["config"],
            types.GenerateContentConfig,
        )

    def test_maps_invalid_key_error_to_actionable_setup_message(self) -> None:
        self.generate_content.side_effect = errors.APIError(
            400,
            {"error": {"message": "API key not valid", "status": "INVALID_ARGUMENT"}},
        )

        with self.assertRaises(HTTPException) as raised:
            main.chat(main.ChatRequest(session_id="session-2", message="Hello"))

        self.assertEqual(raised.exception.status_code, 503)
        self.assertIn("API key is invalid", raised.exception.detail)
        self.assertIn("GEMINI_API_KEY", raised.exception.detail)

    def test_maps_inaccessible_model_to_model_and_project_guidance(self) -> None:
        self.generate_content.side_effect = errors.APIError(
            404,
            {"error": {"message": "Model not found", "status": "NOT_FOUND"}},
        )

        with self.assertRaises(HTTPException) as raised:
            main.chat(main.ChatRequest(session_id="session-3", message="Hello"))

        self.assertEqual(raised.exception.status_code, 503)
        self.assertIn("GEMINI_MODEL", raised.exception.detail)
        self.assertIn("Gemini API access enabled", raised.exception.detail)

    def test_maps_quota_error_separately_from_rate_limit(self) -> None:
        self.generate_content.side_effect = errors.APIError(
            429,
            {"error": {"message": "Request exhausted", "status": "RESOURCE_EXHAUSTED"}},
        )

        with self.assertRaises(HTTPException) as raised:
            main.chat(main.ChatRequest(session_id="session-4", message="Hello"))

        self.assertEqual(raised.exception.status_code, 503)
        self.assertIn("no available quota", raised.exception.detail)

    def test_maps_network_timeout_to_gateway_timeout(self) -> None:
        self.generate_content.side_effect = httpx.ReadTimeout("request timed out")

        with self.assertRaises(HTTPException) as raised:
            main.chat(main.ChatRequest(session_id="session-5", message="Hello"))

        self.assertEqual(raised.exception.status_code, 504)

    def test_rejects_blank_message_without_calling_provider(self) -> None:
        with self.assertRaises(HTTPException) as raised:
            main.chat(main.ChatRequest(session_id="session-6", message="   "))

        self.assertEqual(raised.exception.status_code, 422)
        self.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
