#!/usr/bin/env python3
"""
markdown-indexer.py

This script reads a Markdown file, detects all of its headings, applies a 
custom numbering scheme, and creates a navigable index at the beginning 
of the file. The updated file is then saved as a new Markdown file.

Usage:
    python markdown-indexer.py <markdown_file.md> [options]

Example:
    python markdown-indexer.py README.md 
    python markdown-indexer.py doc.md -o doc-indexed.md

Requirements:
    - Python 3.6+
    - Modules: argparse, re, os
    - Local modules:
        parse_markdown_headers
        header_numarator
        new_headers
        create_index
"""

import argparse
import os

# Import your local modules
from src.parse_markdown_headers import parse_markdown_headers
from src.header_numarator import header_numarator
from src.new_headers import new_headers
from src.create_index import create_index


def main():
    """
    Main function to parse command-line arguments, validate inputs,
    process the Markdown file headings, and produce a new indexed file.
    """
    # 1) Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Generate an index from a markdown file, reorder its headings, "
        "and save a new indexed version."
    )
    parser.add_argument(
        "markdown_file", help="Path to the Markdown file to be indexed."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional path for the output file. "
        "If omitted, '<input-file>-indexed.md' will be used.",
    )

    # Parse arguments
    args = parser.parse_args()

    # 2) Validate the file
    input_file = args.markdown_file

    # Check if file exists
    if not os.path.isfile(input_file):
        parser.error(f"Error: The file '{input_file}' does not exist.")

    # Check if file has .md extension
    if not input_file.lower().endswith(".md"):
        parser.error(f"Error: The file '{input_file}' is not a Markdown (.md) file.")

    # 3) Determine the output file path
    if args.output:
        output_file = args.output
    else:
        # Replace or append '-indexed.md'
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}-indexed.md"

    # 4) Read all lines from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 5) Parse headers and apply transformations
    headers = parse_markdown_headers(input_file)
    headers = header_numarator(headers)
    headers = new_headers(headers)

    # 6) Create the index
    index_list = create_index(headers)

    # 7) Update the original file's lines with new header text
    for header in headers:
        # Header lines are 1-based; list indices are 0-based
        line_index = header["line"] - 1
        lines[line_index] = header["new_text"] + "\n"

    # 8) Construct the index block at the beginning of the file
    index_content = []
    index_content.append(
        lines[0] + "\n"
    )  # Add the first line (usually a title or H1)")
    index_content.append("## Index\n\n")
    for idx_line in index_list:
        index_content.append(idx_line + "\n")

    new_lines = index_content + lines[1:]

    # 9) Write the updated content to the new file
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Indexed file created: {output_file}")


if __name__ == "__main__":
    main()
