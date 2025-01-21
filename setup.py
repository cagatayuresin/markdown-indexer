# setup.py
from setuptools import setup, find_packages

setup(
    name="markdown_indexer",
    version="0.1.0",
    packages=find_packages(),
    requires=[
        "argparse",
        "re",
        "os",
        "unittest",
        "pytest",
        "colorama",
        "coverage",
        "iniconfig",
        "packaging",
        "pluggy",
        "pytest-cov",
        "setuptools",
    ],
)
