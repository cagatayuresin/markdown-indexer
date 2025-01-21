"""
create_index.py

This module provides a function to build a Markdown index (a navigable list)
from the numbered headings. The index uses standard Markdown anchors based
on a simplified slug of the heading text (including numbering if desired).
"""

import re


def create_index(headers):
    """
    Generates a navigable index in Markdown format from a list of heading dicts.
    The anchor is built by converting (header_number + header_text) to a slug:
        1) convert to lowercase
        2) strip non-alphanumeric characters except whitespace and '-'
        3) replace spaces with '-'
        4) reduce multiple hyphens to a single '-'

    Example output:
        - [1. Introduction](#1-introduction)
          - [1.1 Installation](#1-1-installation)
          - [1.2 Configuration](#1-2-configuration)

    Args:
        headers (list of dict): Each dict must have:
            - "header_level" (int)
            - "header_number" (str)
            - "header_text" (str)

    Returns:
        list of str: Lines of Markdown forming an index (each line is a list item).
    """
    index_lines = []

    for header in headers:
        # Indentation based on header_level:
        # Level 1 -> no indent, Level 2 -> 2 spaces, etc.
        indent = "  " * (header["header_level"] - 1)

        # Link text: the visible text in the list
        # If H1 has header_number as "", it will effectively be just the text
        link_text = f"{header['header_number']} {header['header_text']}".strip()

        # Create a slug for the anchor
        anchor_text = link_text.lower()  # 1) to lowercase
        anchor_text = re.sub(r"[^\w\s-]", "", anchor_text)  # 2) remove unwanted chars
        anchor_text = anchor_text.strip().replace(" ", "-")  # 3) spaces -> hyphens
        anchor_text = re.sub(r"-+", "-", anchor_text)  # 4) reduce multiple hyphens

        # If the slug ends up empty, assign a default
        if not anchor_text:
            anchor_text = "header"

        # Build the Markdown link line
        index_line = f"{indent}- [{link_text}](#{anchor_text})"
        index_lines.append(index_line)

    return index_lines
