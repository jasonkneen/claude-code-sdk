"""
Base client implementation for Claude Code SDK
"""

import os
from typing import Dict, Any, Optional

from claude_code_sdk.implementations.cli import ClaudeCliExecutor, ClaudeExecParams
from claude_code_sdk.types import ClaudeCodeOptions, ClaudeCodeError


class BaseClient:
    """Base client for Claude Code SDK"""
    
    def __init__(self, options: Optional[ClaudeCodeOptions] = None):
        """
        Initialize the base client
        
        Args:
            options: Configuration options for the client
        """
        if options is None:
            options = {}
            
        self.api_key = options.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        self.default_model = "claude-code"
        self.default_timeout = options.get("timeout", 300000)  # 5 minutes default
        
        env = {}
        if self.api_key:
            env["ANTHROPIC_API_KEY"] = self.api_key
            
        self.executor = ClaudeCliExecutor(
            cli_path=options.get("cli_path", "@anthropic-ai/claude-code"),
            timeout=self.default_timeout,
            env=env
        )
        
    def create_error(self, message: str, status: int = 500, code: Optional[str] = None) -> ClaudeCodeError:
        """
        Creates an error object in the style of OpenAI/Anthropic SDKs
        
        Args:
            message: Error message
            status: HTTP status code
            code: Error code
            
        Returns:
            ClaudeCodeError: Formatted error object
        """
        error = ClaudeCodeError(message)
        error.status = status
        error.code = code
        return error
    
    def execute_command(self, params: ClaudeExecParams) -> str:
        """
        Executes a Claude CLI command with error handling
        
        Args:
            params: Parameters for the CLI command
            
        Returns:
            str: Command output
            
        Raises:
            ClaudeCodeError: If command execution fails
        """
        try:
            return self.executor.execute(params)
        except Exception as e:
            status = getattr(e, "status", 500)
            raise self.create_error(str(e), status=status)
    
    def execute_stream_command(self, params: ClaudeExecParams):
        """
        Creates a streaming response from Claude CLI
        
        Args:
            params: Parameters for the CLI command
            
        Returns:
            Generator: Stream of response chunks
        """
        return self.executor.execute_stream(params)