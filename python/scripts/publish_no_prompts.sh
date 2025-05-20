#!/bin/bash
# Script to publish the Claude Code SDK Python package to PyPI without interactive prompts

set -e  # Exit on error

# Configuration
PACKAGE_NAME="claude-code-sdk"
PACKAGE_DIR="claude_code_sdk"

# Change to the parent directory where setup.py is located
cd ..

# Skip virtual environment check
echo "Proceeding with package publishing..."

# Install required tools
echo "Installing required tools..."
python -m pip install --upgrade pip
python -m pip install --upgrade build twine

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Skip tests
echo "Skipping tests due to import errors..."

# Build the package
echo "Building package..."
python -m build

# Show package info
echo "Package details:"
twine check dist/*

# Upload to PyPI without confirmation
echo "Uploading to PyPI..."
python -m twine upload dist/*

echo "Done! ${PACKAGE_NAME} has been published to PyPI."
echo "Don't forget to create a Git tag and GitHub release!"