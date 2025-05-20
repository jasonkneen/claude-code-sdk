"""
Claude Code SDK - Python wrapper for Claude Code CLI
"""

from claude_code_sdk.client import ClaudeCode
from claude_code_sdk.exceptions import (
    ClaudeCodeError,
    AuthenticationError,
    RateLimitError,
    APIError,
    InvalidRequestError,
    TimeoutError,
    ToolError
)
from claude_code_sdk.logging import configure_logging
from claude_code_sdk.utils import get_sdk_version, get_cli_version, is_cli_installed

__version__ = "0.1.0"
__all__ = [
    "ClaudeCode",
    "ClaudeCodeError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "InvalidRequestError",
    "TimeoutError",
    "ToolError",
    "configure_logging",
    "get_sdk_version",
    "get_cli_version",
    "is_cli_installed"
]