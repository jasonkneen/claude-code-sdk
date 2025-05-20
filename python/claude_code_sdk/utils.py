"""
Utility functions for Claude Code SDK
"""

import os
import json
import tempfile
import platform
import subprocess
from typing import Dict, Any, List, Optional, Union, Tuple

from claude_code_sdk.exceptions import InvalidRequestError, APIError


def get_sdk_version() -> str:
    """Get the SDK version"""
    from claude_code_sdk import __version__
    return __version__


def get_cli_version(cli_path: str = "@anthropic-ai/claude-code") -> str:
    """
    Get the Claude CLI version
    
    Args:
        cli_path: Path to the Claude CLI executable
        
    Returns:
        str: CLI version
        
    Raises:
        APIError: If CLI version check fails
    """
    try:
        result = subprocess.run(
            [cli_path, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise APIError(f"Failed to get CLI version: {e.stderr}")
    except FileNotFoundError:
        raise APIError(f"Claude CLI not found at path: {cli_path}")


def get_system_info() -> Dict[str, str]:
    """
    Get system information
    
    Returns:
        Dict[str, str]: System information
    """
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "sdk_version": get_sdk_version(),
    }


def is_cli_installed(cli_path: str = "@anthropic-ai/claude-code") -> bool:
    """
    Check if Claude CLI is installed
    
    Args:
        cli_path: Path to the Claude CLI executable
        
    Returns:
        bool: True if CLI is installed
    """
    try:
        subprocess.run(
            [cli_path, "--help"],
            capture_output=True,
            text=True,
            check=False
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def create_temp_file(content: str, suffix: str = ".txt") -> str:
    """
    Create a temporary file with content
    
    Args:
        content: File content
        suffix: File suffix
        
    Returns:
        str: Path to temporary file
    """
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    except Exception as e:
        # Clean up the file if writing fails
        try:
            os.unlink(path)
        except:
            pass
        raise APIError(f"Failed to create temporary file: {str(e)}")


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Read and parse JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dict[str, Any]: Parsed JSON data
        
    Raises:
        InvalidRequestError: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise InvalidRequestError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise InvalidRequestError(f"Invalid JSON in file {file_path}: {str(e)}")
    except Exception as e:
        raise APIError(f"Error reading file {file_path}: {str(e)}")


def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Write data to JSON file
    
    Args:
        file_path: Path to JSON file
        data: Data to write
        
    Raises:
        APIError: If file cannot be written
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise APIError(f"Error writing to file {file_path}: {str(e)}")


def sanitize_file_path(path: str) -> str:
    """
    Sanitize file path for security
    
    Args:
        path: File path to sanitize
        
    Returns:
        str: Sanitized file path
        
    Raises:
        InvalidRequestError: If path contains invalid characters
    """
    # Check for path traversal attempts
    if ".." in path.split(os.sep):
        raise InvalidRequestError("Path contains invalid directory traversal")
    
    # Normalize path
    normalized = os.path.normpath(path)
    
    # Check for suspicious characters
    if any(c in normalized for c in ['|', '&', ';', '$', '`', '\\']):
        raise InvalidRequestError("Path contains invalid characters")
        
    return normalized