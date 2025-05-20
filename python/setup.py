"""
Setup script for Claude Code SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-sdk",
    version="0.1.0",
    author="Anthropic",
    author_email="info@anthropic.com",
    description="Python wrapper for Claude Code CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthropics/claude-code-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
)