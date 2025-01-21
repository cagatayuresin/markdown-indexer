"""
parse_markdown_headers.py

This module provides a function to parse Markdown headings from a file, while
ignoring any headings that appear inside fenced code blocks (triple-backtick blocks).
"""

import re


def parse_markdown_headers(file_path):
    """
    Parses the specified Markdown file to extract heading information.

    Headings are identified by lines that match the pattern:
        ^(#{1,6})\s+(.*)$

    The function also skips headings located inside fenced code blocks
    (denoted by lines containing triple backticks: ```).

    Args:
        file_path (str): Path to the Markdown (.md) file.

    Returns:
        list of dict: A list of dictionaries, where each dictionary contains:
            {
                "line": (int) 1-based line number of the heading in the file,
                "header_level": (int) heading level (1 to 6),
                "header_text": (str) the raw text of the heading (excluding the #)
            }
    """
    headers = []

    # Temporary dictionary for storing heading info
    temp = {
        "line": 0,
        "header_level": 0,
        "header_text": "",
    }

    # Regex pattern for capturing headings: 1 to 6 '#' characters,
    # followed by space(s), then the heading text.
    header_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

    with open(file_path, "r", encoding="utf-8") as file:
        in_code_block = False

        for line_num, line in enumerate(file, start=1):
            # Check if we are toggling in/out of a fenced code block
            if "```" in line:
                in_code_block = not in_code_block

            # If we're not inside a code block, test for a heading
            if not in_code_block:
                match = header_pattern.match(line)
                if match:
                    header_level = len(match.group(1))
                    header_text = match.group(2).strip()

                    temp["line"] = line_num
                    temp["header_level"] = header_level
                    temp["header_text"] = header_text

                    headers.append(temp.copy())

    return headers
