"""
Type definitions for Claude Code SDK
"""

from typing import Dict, List, Any, Optional, TypedDict, Union
from typing_extensions import NotRequired


class ClaudeCodeError(Exception):
    """Claude Code error with status code and error code"""
    status: int
    code: Optional[str]


class ClaudeCodeOptions(TypedDict, total=False):
    """Options for Claude Code client"""
    api_key: NotRequired[Optional[str]]
    cli_path: NotRequired[Optional[str]]
    timeout: NotRequired[Optional[int]]


class OpenAIMessage(TypedDict, total=False):
    """OpenAI-style message"""
    role: str
    content: str
    name: NotRequired[Optional[str]]
    tool_call_id: NotRequired[Optional[str]]


class AnthropicContentBlock(TypedDict, total=False):
    """Anthropic content block"""
    type: str
    text: NotRequired[Optional[str]]
    source: NotRequired[Optional[Dict[str, Any]]]


class AnthropicMessage(TypedDict, total=False):
    """Anthropic-style message"""
    role: str
    content: Union[str, List[AnthropicContentBlock]]
    name: NotRequired[Optional[str]]


class ToolDefinition(TypedDict, total=False):
    """Tool definition"""
    name: str
    description: NotRequired[Optional[str]]
    input_schema: NotRequired[Dict[str, Any]]