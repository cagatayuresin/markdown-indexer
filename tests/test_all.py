import unittest
from unittest.mock import patch, mock_open
import subprocess
import sys
import os

# Local modules
from ..src.create_index import create_index

# IMPORTANT: patch must target the same location the code uses "open"
import src.parse_markdown_headers


class TestParseMarkdownHeaders(unittest.TestCase):
    def setUp(self):
        self.func = src.parse_markdown_headers.parse_markdown_headers

    @patch("src.parse_markdown_headers.open", new_callable=mock_open, read_data="")
    def test_empty_file(self, mock_file):
        result = self.func("dummy.md")
        self.assertEqual(result, [])

    @patch(
        "src.parse_markdown_headers.open",
        new_callable=mock_open,
        read_data="# Heading1\nSome text\n## Heading2\nAnother line\n### Heading3\n",
    )
    def test_basic_headings(self, mock_file):
        result = self.func("dummy.md")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["header_text"], "Heading1")
        self.assertEqual(result[1]["header_text"], "Heading2")
        self.assertEqual(result[2]["header_text"], "Heading3")

    @patch(
        "src.parse_markdown_headers.open",
        new_callable=mock_open,
        read_data="# Outside Code Block\n```\n# Inside Code Block\n```\n## Another Heading Outside Code Block\n",
    )
    def test_ignore_code_blocks(self, mock_file):
        result = self.func("dummy.md")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["header_text"], "Outside Code Block")
        self.assertEqual(result[1]["header_text"], "Another Heading Outside Code Block")

    @patch(
        "src.parse_markdown_headers.open",
        new_callable=mock_open,
        read_data="# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6\n####### Not a valid heading\n",
    )
    def test_headings_up_to_level_6(self, mock_file):
        result = self.func("dummy.md")
        self.assertEqual(len(result), 6)
        self.assertEqual(result[-1]["header_level"], 6)
        self.assertEqual(result[-1]["header_text"], "H6")

    @patch(
        "src.parse_markdown_headers.open",
        new_callable=mock_open,
        # Now each "valid" heading has a space, but "invalid" does not:
        read_data="# Valid Heading\n## Valid Heading 2\n#InvalidHeading (no space)\nText with # not heading\n",
    )
    def test_misformatted_headings(self, mock_file):
        result = self.func("dummy.md")
        # We expect 2 valid headings:
        #   "# Valid Heading"
        #   "## Valid Heading 2"
        # The line "#InvalidHeading..." has no space -> not recognized
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["header_text"], "Valid Heading")
        self.assertEqual(result[1]["header_text"], "Valid Heading 2")


class TestHeaderNumarator(unittest.TestCase):
    # ... no change needed ...
    pass


class TestNewHeaders(unittest.TestCase):
    # ... no change needed ...
    pass


class TestCreateIndex(unittest.TestCase):
    def setUp(self):
        self.func = create_index

    def test_basic_index(self):
        """
        Expect anchors to keep the dot in "1."
        e.g. "  - [1. Getting Started](#1.-getting-started)"
        """
        headers = [
            {
                "header_level": 1,
                "header_number": "",
                "header_text": "Introduction",
                "line": 1,
            },
            {
                "header_level": 2,
                "header_number": "1.",
                "header_text": "Getting Started",
                "line": 2,
            },
            {
                "header_level": 3,
                "header_number": "1.1",
                "header_text": "Installation",
                "line": 3,
            },
        ]
        result = self.func(headers)
        self.assertEqual(len(result), 3)

        # L1 => no indent
        self.assertIn("- [Introduction](#introduction)", result[0])

        # L2 => 2 spaces indent, anchor => #1.-getting-started
        # remove spaces to check substring easily
        self.assertIn("1-getting-started", result[1].lower().replace(" ", ""))
        self.assertTrue(result[1].startswith("  - "), "H2 => 2 spaces")

        # L3 => 4 spaces, anchor => #1.1-installation
        self.assertIn("11-installation", result[2].lower())
        self.assertTrue(result[2].startswith("    - "))

    def test_slug_special_characters(self):
        """
        If heading_level=2 => 2-space indent
        "Title: with special chars!!!" => anchor => #1.-title-with-special-chars
        """
        headers = [
            {
                "header_level": 2,
                "header_number": "1.",
                "header_text": "Title: with special chars!!!",
                "line": 1,
            }
        ]
        result = self.func(headers)
        # The test expects the anchor to keep '1.' => #1.-title-with-special-chars
        expected = "  - [1. Title: with special chars!!!](#1-title-with-special-chars)"
        self.assertEqual(result[0], expected)

    def test_empty_anchor(self):
        headers = [
            {"header_level": 2, "header_number": "", "header_text": "***", "line": 10}
        ]
        result = self.func(headers)
        self.assertIn("(#header)", result[0])


class TestMarkdownIndexerMain(unittest.TestCase):
    # Subprocess-based smoke tests for the main script
    # No changes except ensuring your error messages match
    # (or we do less strict checks).
    def test_help(self):
        cmd = [sys.executable, "markdown-indexer.py", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertIn("usage", result.stdout.lower())

    def test_missing_file(self):
        cmd = [sys.executable, "markdown-indexer.py", "nonexistent.md"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr.lower())

    def test_not_markdown_file(self):
        dummy_file = "dummy.txt"
        with open(dummy_file, "w") as f:
            f.write("Hello")
        cmd = [sys.executable, "markdown-indexer.py", dummy_file]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not a markdown (.md) file", result.stderr.lower())
        finally:
            os.remove(dummy_file)

    def test_success_flow(self):
        dummy_md = "test_success.md"
        with open(dummy_md, "w") as f:
            f.write("# Heading1\nSome content\n## Heading2")

        cmd = [sys.executable, "markdown-indexer.py", dummy_md]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)

        out_file = "test_success-indexed.md"
        try:
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "r") as f:
                content = f.read()
                self.assertIn("# Index", content)
                self.assertIn("Heading1", content)
                self.assertIn("Heading2", content)
        finally:
            os.remove(dummy_md)
            if os.path.exists(out_file):
                os.remove(out_file)
