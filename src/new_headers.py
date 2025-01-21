"""
new_headers.py

This module provides a function to build the "new_text" of each heading, 
combining the Markdown hashes, the assigned numbering (if any), and the header text itself.
"""


def new_headers(headers):
    """
    Creates the final text version of each heading and stores it in "new_text".
    For level 1 headings, it simply keeps '#' plus the original text.
    For others, it includes the numbering (e.g., '1.', '1.2', etc.) after the '#' characters.

    Args:
        headers (list of dict): Output from header_numarator. Each dict is expected to have:
            - "header_level" (int)
            - "header_text" (str)
            - "header_number" (str)

    Returns:
        list of dict: The same list but with the "new_text" field set for each header.
    """
    for header in headers:
        if header["header_level"] == 1:
            # For H1, no numbering is added
            header["new_text"] = f"# {header['header_text']}"
        else:
            # For H2-H6, add the numbering between the '#' and the text
            header["new_text"] = (
                f"{header['header_level'] * '#'} {header['header_number']} {header['header_text']}"
            )

    return headers
