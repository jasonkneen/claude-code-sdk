# Contributing to Claude Code SDK (Python)

Thank you for your interest in contributing to the Claude Code SDK! This document provides guidelines and instructions for contributing to the Python implementation.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. **Fork the repository** and clone it locally
2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install in development mode**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # Install development dependencies
   ```
4. **Run tests**:
   ```bash
   pytest
   ```

## Development Workflow

1. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Write tests** for your changes

4. **Run linting and type checking**:
   ```bash
   mypy claude_code_sdk
   flake8 claude_code_sdk
   black --check claude_code_sdk
   ```

5. **Format your code**:
   ```bash
   black claude_code_sdk
   isort claude_code_sdk
   ```

6. **Commit your changes** with a descriptive commit message

7. **Push your branch** and submit a pull request

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write docstrings for all public functions, methods, and classes
- Use snake_case for variables/functions and PascalCase for classes
- Handle errors appropriately with specific exception types
- Use async/await for streaming operations where appropriate

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Mock external dependencies in tests
- Use pytest fixtures for common test setup

## Documentation

- Update documentation for any changed functionality
- Document all public APIs with docstrings
- Include examples for new features
- Follow Google-style docstring format

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update the README.md with details of changes if appropriate
3. The PR should work on the main branch
4. Include a description of the changes in your PR

## Release Process

Releases are managed by the maintainers. The general process is:

1. Update version in `__init__.py` and setup.py
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Publish to PyPI

## Getting Help

If you have questions or need help, please open an issue on GitHub.

Thank you for contributing to the Claude Code SDK!