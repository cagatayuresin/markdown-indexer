# Markdown Indexer

![Build Status](https://github.com/cagatayuresin/markdown-indexer/actions/workflows/tests.yml/badge.svg) [![Quality Gate Status](https://sonarqube.cagatayuresin.com/api/project_badges/measure?project=cagatayuresin_markdown-indexer_AZSGohgaoWE6bsN4ROvT&metric=alert_status&token=sqb_c7267edf829b2231f7d6a5c515d284effba30be4)](https://sonarqube.cagatayuresin.com/dashboard?id=cagatayuresin_markdown-indexer_AZSGohgaoWE6bsN4ROvT) [![Coverage](https://sonarqube.cagatayuresin.com/api/project_badges/measure?project=cagatayuresin_markdown-indexer_AZSGohgaoWE6bsN4ROvT&metric=coverage&token=sqb_c7267edf829b2231f7d6a5c515d284effba30be4)](https://sonarqube.cagatayuresin.com/dashboard?id=cagatayuresin_markdown-indexer_AZSGohgaoWE6bsN4ROvT) ![License](https://img.shields.io/github/license/cagatayuresin/markdown-indexer.svg) ![Python Version](https://img.shields.io/badge/python-3.12.6-blue.svg)

This repository contains a set of Python scripts and modules that analyze a Markdown file, extract its headings, automatically number them, and generate a navigable index. The index is then inserted into the final output file. This tool helps keep large documentation files organized and easy to navigate.

---

## Features

- **Automated Heading Numbering**  
  Headings can be numbered hierarchically (e.g., `1.`, `1.1`, `1.2`, `1.2.1`, etc.), based on their level (H1, H2, etc.).

- **Ignore Code Blocks**  
  Headings placed inside fenced code blocks (```) are skipped, so they don't appear as real headings in your final output.

- **Anchored Table of Contents**  
  Creates an index section in Markdown with clickable links, leading directly to the corresponding headings. The links are automatically slugified.

- **Easy Command-line Integration**  
  The main script uses `argparse` to accept the input Markdown file and optional output file path.

---

## Requirements

- **Python 3.6+**  
  For f-string support and modern Python features.

- **Dependencies**  
  - Standard libraries: `os`, `argparse`, `re`
  - Local modules:
    - `parse_markdown_headers`
    - `header_numarator`
    - `new_headers`
    - `create_index`

---

## Installation

1. Clone or download this repository into your local environment.
2. (Optional) Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   # or
   venv\Scripts\activate      # On Windows
   ```

3. Install any necessary dependencies (if not already included).

---

## Usage

The main script is `markdown-indexer.py`, which you can run from the command line. It requires one positional argument for the Markdown file you want to process.

```bash
python markdown-indexer.py <markdown_file.md> [options]
```

**Arguments**:  

- `<markdown_file.md>`  
  The path to the input Markdown file. Must have a `.md` extension.

**Options**:

- `-o` or `--output`  
  Specify a custom output filename. If omitted, the program appends `-indexed.md` to the original filename.

Example:

```bash
python markdown-indexer.py README.md -o README-indexed.md
```

This command reads all headings from `README.md`, numbers them, creates a table of contents, and places the table of contents at the beginning of the file. The updated version is then saved as `README-indexed.md`.

---

## Project Structure

```plaintext
project/
├─ src/
│  ├─ parse_markdown_headers.py
│  ├─ header_numarator.py
│  ├─ new_headers.py
│  └─ create_index.py
├─ markdown-indexer.py
└─ tests/
   └─ test_all.py
```

- **markdown-indexer.py**  
  Main script that orchestrates reading, transforming, and writing the Markdown file.
- **parse_markdown_headers.py**  
  Identifies headings in the Markdown file while ignoring fenced code blocks.
- **header_numarator.py**  
  Generates a hierarchical numbering (e.g., `1.`, `1.1`, etc.) for headings.
- **new_headers.py**  
  Builds the final string for each heading, combining `#` characters, numbering, and the original text.
- **create_index.py**  
  Produces a list of Markdown-friendly index lines with clickable links (anchors).

---

## Testing

The project is designed with high coverage unit tests (not shown in this README). To run tests, you can include a `tests` folder or a `test_*.py` file that uses `unittest` or `pytest`. For instance:

```bash
pytest --cov=src --cov-report=term-missing
```

This command would run all tests and display coverage information if you have `pytest` and `pytest-cov` installed.

---

## Contributing

1. **Fork** the project.  
2. Create a new **feature branch**.  
3. **Commit** your changes with clear messages.  
4. Submit a **Pull Request** detailing what changes you've made and why.

---

## License

This project is licensed under the MIT License. You are free to copy, modify, merge, publish, or distribute this software, subject to the conditions of the MIT license.

For details, see the **LICENSE** file in the repository.
