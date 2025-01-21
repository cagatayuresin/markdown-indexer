"""
header_numarator.py

This module provides a function to generate hierarchical numbering 
for Markdown headings. For instance:
    - Level 2 heading might become "1."
    - Level 3 heading under "1." becomes "1.1"
    - Level 4 heading under "1.1" becomes "1.1.1"
... and so on.
"""


def header_numarator(headers):
    """
    Assigns a hierarchical numbering (like 1., 1.1, 1.1.1, etc.) to each heading
    according to its level. The numbering is stored in "header_number" key
    within the headers list.

    Args:
        headers (list of dict): Output from parse_markdown_headers.
                                Each dict must have "header_level".

    Returns:
        list of dict: The same list of headers, but with "header_number" field added.
    """
    # Track numbering count for levels 1 to 6
    level_counts = [0, 0, 0, 0, 0, 0]

    for header in headers:
        level = header["header_level"]

        # For top-level heading (H1), we typically don't assign a number
        if level == 1:
            header["header_number"] = ""
        else:
            # Increase the count for this level
            level_counts[level - 1] += 1

            # Reset lower-level counts
            for i in range(level, len(level_counts)):
                level_counts[i] = 0

            # Build the numbering string from level 2 upward
            numbering_parts = [str(level_counts[i]) for i in range(1, level)]
            numbering_str = ".".join(numbering_parts)

            # For example, if numbering_parts = ["1"], we might want "1."
            # Some prefer to skip the trailing dot, adapt as you wish.
            if len(numbering_parts) == 1:
                numbering_str += "."

            header["header_number"] = numbering_str

    return headers
