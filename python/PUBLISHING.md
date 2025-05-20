# Publishing to PyPI

This guide explains how to publish the Claude Code SDK Python package to PyPI.

## Prerequisites

1. Make sure you have a PyPI account
2. Install required publishing tools:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install --upgrade build twine
   ```
3. If you want to test before publishing to the main PyPI, register on TestPyPI: https://test.pypi.org/account/register/

## Update Version and Documentation

1. Update the version number in `setup.py`
2. Update any necessary documentation
3. Make sure all tests pass:
   ```bash
   pytest
   ```

## Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

This creates source and wheel distributions in the `dist/` directory.

## Test the Package (Optional)

Upload to TestPyPI first to verify everything works:

```bash
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI to verify:

```bash
pip install --index-url https://test.pypi.org/simple/ claude-code-sdk
```

## Publish to PyPI

Once you're confident everything is working correctly:

```bash
# Upload the package to PyPI
python -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

### Security Best Practices

Avoid typing your password in the terminal by using one of these methods:

1. Configure a PyPI token in your `.pypirc` file:
   ```
   [pypi]
   username = __token__
   password = pypi-xxx...
   ```

2. Use environment variables:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-xxx...
   python -m twine upload dist/*
   ```

3. Use keyring to securely store credentials:
   ```bash
   pip install keyring
   keyring set https://upload.pypi.org/legacy/ your-username your-password
   python -m twine upload dist/*
   ```

## Verify the Upload

Check that your package appears on PyPI:
https://pypi.org/project/claude-code-sdk/

## Install from PyPI

Users can now install your package using:

```bash
pip install claude-code-sdk
```

## Creating a GitHub Release

After publishing to PyPI:

1. Create a new tag matching the version:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. Create a release on GitHub with release notes