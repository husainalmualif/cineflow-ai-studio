#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the bundled FastMCP Omni Flash Video Agent (`mcp/server.py`).

Compatible with both `pytest -v tests/test_omni_agent.py` and direct CLI execution:
`python tests/test_omni_agent.py` (even in bare CI environments without `google-genai` or `mcp` installed).
"""
# pylint: disable=unused-import,too-few-public-methods,missing-function-docstring,protected-access,consider-using-with

from __future__ import annotations

import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT_DIR = Path(__file__).resolve().parent.parent
MCP_DIR = ROOT_DIR / "mcp"
SCRIPTS_DIR = ROOT_DIR / "scripts"
sys.path.insert(0, str(MCP_DIR))
sys.path.insert(0, str(SCRIPTS_DIR))

os.environ.setdefault("GEMINI_API_KEY", "test-key")

# Provide lightweight fallback stubs if google-genai or fastmcp are not installed in bare CI
try:
    import google.genai  # noqa: F401
except ImportError:
    google_pkg = types.ModuleType("google")
    genai_mod = types.ModuleType("google.genai")
    genai_mod.Client = MagicMock(return_value=MagicMock())  # type: ignore[attr-defined]
    google_pkg.genai = genai_mod  # type: ignore[attr-defined]
    sys.modules.setdefault("google", google_pkg)
    sys.modules.setdefault("google.genai", genai_mod)

try:
    import mcp.server.fastmcp  # noqa: F401
except ImportError:
    mcp_pkg = types.ModuleType("mcp")
    mcp_server_pkg = types.ModuleType("mcp.server")
    fastmcp_mod = types.ModuleType("mcp.server.fastmcp")

    class _FakeTool:
        def __init__(self, name: str) -> None:
            self.name = name

    class _FakeToolManager:
        def __init__(self) -> None:
            self._tools: list[_FakeTool] = []

        def list_tools(self) -> list[_FakeTool]:
            return list(self._tools)

    class _FakeFastMCP:
        def __init__(self, name: str) -> None:
            self.name = name
            self._tool_manager = _FakeToolManager()

        def tool(self):
            def _decorator(fn):
                self._tool_manager._tools.append(_FakeTool(fn.__name__))
                return fn

            return _decorator

        def run(self) -> None:
            pass

    fastmcp_mod.FastMCP = _FakeFastMCP  # type: ignore[attr-defined]
    mcp_server_pkg.fastmcp = fastmcp_mod  # type: ignore[attr-defined]
    mcp_pkg.server = mcp_server_pkg  # type: ignore[attr-defined]
    sys.modules.setdefault("mcp", mcp_pkg)
    sys.modules.setdefault("mcp.server", mcp_server_pkg)
    sys.modules.setdefault("mcp.server.fastmcp", fastmcp_mod)

import server  # noqa: E402
from server import (  # noqa: E402
    MODEL_NAME,
    _get_client,
    _get_image_data,
    animate_image,
    edit_user_video,
    edit_video,
    generate_video,
    generate_with_subjects,
    get_help,
    interpolate_images,
    mcp,
    upload_to_youtube,
)
from studio_config import OMNI_FLASH_MODEL_DEFAULT  # noqa: E402


class TestOmniVideoAgent(unittest.TestCase):
    """Comprehensive mocked unit test suite for mcp/server.py."""

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_image_path = os.path.join(self.test_dir.name, "test.png")
        with open(self.test_image_path, "wb") as f:
            f.write(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
            )

    def tearDown(self):
        self.test_dir.cleanup()

    def _mock_interaction(self, interaction_id="int_123", data="ZHVtbXlfdmlkZW8=", uri=None):
        interaction = MagicMock()
        interaction.id = interaction_id
        if data is None and uri is None:
            interaction.output_video = None
        else:
            interaction.output_video = MagicMock()
            interaction.output_video.data = data
            interaction.output_video.uri = uri
        return interaction

    def test_default_model_matches_studio_config(self):
        """Verify server MODEL_NAME reads default from studio_config.OMNI_FLASH_MODEL_DEFAULT."""
        self.assertEqual(MODEL_NAME, OMNI_FLASH_MODEL_DEFAULT)

    def test_lazy_client_raises_clear_error_without_api_key(self):
        """Verify _get_client() is lazy and raises a clear RuntimeError if no API key is configured."""
        with patch.object(server, "client", None):
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(RuntimeError) as ctx:
                    _get_client()
                self.assertIn("Missing Gemini API key", str(ctx.exception))

    def test_get_image_data_valid(self):
        """Test image encoding helper with a valid image file."""
        data = _get_image_data(self.test_image_path)
        self.assertEqual(data["type"], "image")
        self.assertEqual(data["mime_type"], "image/png")
        self.assertTrue(len(data["data"]) > 0)

    def test_get_image_data_missing(self):
        """Test image encoding helper raises FileNotFoundError if file is missing."""
        with self.assertRaises(FileNotFoundError):
            _get_image_data("non_existent_file.png")

    @patch("server.client")
    def test_generate_video_success(self, mock_client):
        """Test generate_video tool with mocked Interactions API response."""
        mock_client.interactions.create.return_value = self._mock_interaction()

        with patch("server.open", unittest.mock.mock_open()):
            result = generate_video(prompt="test prompt", aspect_ratio="16:9")
        self.assertIn("🟢 Video successfully saved!", result)
        self.assertIn("int_123", result)
        self.assertIn("Delivery mode: inline", result)
        create_kwargs = mock_client.interactions.create.call_args.kwargs
        self.assertEqual(create_kwargs["response_format"]["aspect_ratio"], "16:9")
        self.assertTrue(create_kwargs["store"])

    @patch("server.client")
    def test_generate_video_uri_delivery_polls_file_api(self, mock_client):
        """Test generate_video with delivery='uri' extracts clean file ID and polls until ACTIVE."""
        mock_client.interactions.create.return_value = self._mock_interaction(
            interaction_id="v1_uri_999",
            data=None,
            uri="https://generativelanguage.googleapis.com/v1beta/files/abc987xyz:download?alt=media",
        )
        active_file = MagicMock()
        active_file.state.name = "ACTIVE"
        mock_client.files.get.return_value = active_file
        mock_client.files.download.return_value = b"fake_mp4_bytes"

        with patch("server.open", unittest.mock.mock_open()):
            result = generate_video(prompt="high motion scene", aspect_ratio="9:16", delivery="uri")
        self.assertIn("🟢 Video successfully saved!", result)
        self.assertIn("Delivery mode: uri", result)
        self.assertIn("v1_uri_999", result)
        mock_client.files.get.assert_called_with(name="files/abc987xyz")
        mock_client.files.download.assert_called_with(file="files/abc987xyz")

    @patch("server.client")
    def test_generate_video_no_output_video(self, mock_client):
        """Test generate_video tool when no output video is returned by the API."""
        mock_client.interactions.create.return_value = self._mock_interaction(data=None)

        result = generate_video(prompt="test prompt")
        self.assertIn("🟢 Interaction completed successfully.", result)
        self.assertIn("No direct video output was found", result)

    @patch("server.client")
    def test_generate_video_failure(self, mock_client):
        """Test generate_video tool gracefully handles exceptions."""
        mock_client.interactions.create.side_effect = RuntimeError("API Key expired")

        result = generate_video(prompt="test prompt")
        self.assertIn("🔴 Generation failed: API Key expired", result)

    @patch("server.client")
    def test_edit_video_success(self, mock_client):
        """Test edit_video tool chains the previous interaction ID and omits aspect_ratio."""
        mock_client.interactions.create.return_value = self._mock_interaction(
            interaction_id="int_456"
        )

        with patch("server.open", unittest.mock.mock_open()):
            result = edit_video(
                previous_interaction_id="int_123", edit_prompt="make it rain"
            )
        self.assertIn("🟢 Video successfully saved!", result)
        self.assertIn("int_456", result)
        create_kwargs = mock_client.interactions.create.call_args.kwargs
        self.assertEqual(create_kwargs["previous_interaction_id"], "int_123")
        self.assertNotIn("aspect_ratio", create_kwargs["response_format"])

    @patch("server.client")
    def test_animate_interpolate_and_subjects(self, mock_client):
        """Test animate_image, interpolate_images, and generate_with_subjects multimodal inputs."""
        mock_client.interactions.create.return_value = self._mock_interaction(
            interaction_id="int_789"
        )
        real_data = _get_image_data(self.test_image_path)
        with patch("server._get_image_data", return_value=real_data):
            with patch("server.open", unittest.mock.mock_open()):
                res_anim = animate_image(image_path=self.test_image_path, motion_prompt="slow pan")
                res_interp = interpolate_images(
                    start_image_path=self.test_image_path,
                    end_image_path=self.test_image_path,
                    prompt="sunrise to sunset",
                )
                res_subj = generate_with_subjects(
                    subject_image_paths=[self.test_image_path, self.test_image_path],
                    prompt="both subjects walking",
                )
        self.assertIn("🟢 Video successfully saved!", res_anim)
        self.assertIn("🟢 Video successfully saved!", res_interp)
        self.assertIn("🟢 Video successfully saved!", res_subj)

    @patch("server.client")
    def test_animate_image_missing_file(self, mock_client):
        """Test animate_image returns an error string for a missing image."""
        result = animate_image(image_path="missing.png", motion_prompt="pan")
        self.assertIn("🔴 Animation failed:", result)
        mock_client.interactions.create.assert_not_called()

    def test_edit_user_video_missing_file(self):
        """Test edit_user_video returns an error string for a missing video file."""
        res = edit_user_video(video_path="missing_clip.mp4", edit_prompt="Pixar style")
        self.assertIn("🔴 Video file not found:", res)

    def test_upload_to_youtube_missing_video_and_credentials(self):
        """Test upload_to_youtube validates video path and uses JSON credentials (no pickle)."""
        res_missing = upload_to_youtube(
            video_path="non_existent_video.mp4",
            title="Test",
            description="Test",
        )
        self.assertIn("❌ Error: Video file not found", res_missing)

        dummy_video = os.path.join(self.test_dir.name, "clip.mp4")
        with open(dummy_video, "wb") as f:
            f.write(b"0000")
        res_no_creds = upload_to_youtube(
            video_path=dummy_video,
            title="Test",
            description="Test",
        )
        self.assertIn("YouTube API credentials missing", res_no_creds)

    def test_mcp_tools_registered(self):
        """Verify that the expected 8 tools are registered to the FastMCP server."""
        tools = [t.name for t in mcp._tool_manager.list_tools()]
        for tool in [
            "generate_video",
            "edit_video",
            "animate_image",
            "interpolate_images",
            "generate_with_subjects",
            "edit_user_video",
            "upload_to_youtube",
            "get_help",
        ]:
            self.assertIn(tool, tools)

    def test_get_help(self):
        """Verify that get_help documents every exposed tool and delivery modes."""
        result = get_help()
        for tool in [
            "generate_video",
            "edit_video",
            "animate_image",
            "interpolate_images",
            "generate_with_subjects",
            "edit_user_video",
            "upload_to_youtube",
            "get_help",
        ]:
            self.assertIn(tool, result)
        self.assertIn("Delivery Modes", result)


if __name__ == "__main__":
    unittest.main()
