"""
Improved CLI executor for Claude Code SDK with better error handling and retry logic
"""

import os
import json
import subprocess
import logging
from typing import Dict, Any, List, Optional, Union, Generator

from claude_code_sdk.exceptions import (
    ClaudeCodeError, 
    AuthenticationError,
    RateLimitError,
    APIError,
    InvalidRequestError,
    TimeoutError,
    map_error_code_to_exception
)
from claude_code_sdk.retry import retry_with_backoff
from claude_code_sdk.validation import validate_required, validate_enum

# Configure logger
logger = logging.getLogger("claude_code_sdk.cli")


class ClaudeExecOptions:
    """Options for Claude CLI executor"""
    cli_path: str
    timeout: int
    env: Dict[str, str]
    max_retries: int
    retry_codes: List[int]


class ClaudeCliExecutor:
    """Executor for Claude CLI commands with improved error handling"""
    
    def __init__(
        self, 
        cli_path: str = "@anthropic-ai/claude-code", 
        timeout: int = 300000, 
        env: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
        retry_codes: Optional[List[int]] = None
    ):
        """
        Initialize the CLI executor
        
        Args:
            cli_path: Path to the Claude CLI executable
            timeout: Default timeout in milliseconds
            env: Environment variables
            max_retries: Maximum number of retries for transient errors
            retry_codes: HTTP status codes to retry on
        """
        self.cli_path = cli_path
        self.default_timeout = timeout
        self.env = {**os.environ, **(env or {})}
        self.max_retries = max_retries
        self.retry_codes = retry_codes or [429, 500, 502, 503, 504]
        
        # Validate API key
        if "ANTHROPIC_API_KEY" not in self.env:
            logger.warning("ANTHROPIC_API_KEY not found in environment variables")
            
        # Check if CLI is installed
        self._check_cli_installed()
        
    def _check_cli_installed(self) -> None:
        """
        Check if Claude CLI is installed
        
        Raises:
            APIError: If CLI is not installed
        """
        try:
            subprocess.run(
                [self.cli_path, "--help"],
                env=self.env,
                capture_output=True,
                text=True,
                check=False
            )
        except FileNotFoundError:
            raise APIError(
                f"Claude CLI not found at path: {self.cli_path}. "
                "Please install it with: npm install -g @anthropic-ai/claude-code"
            )
        
    def _build_args(self, params: Dict[str, Any]) -> List[str]:
        """
        Build command line arguments from parameters
        
        Args:
            params: Command parameters
            
        Returns:
            List[str]: Command line arguments
        """
        args = []
        
        if params.get("prompt"):
            args.extend(["-p", params["prompt"]])
            
        if params.get("output_format"):
            validate_enum(
                params["output_format"],
                ["text", "json", "stream-json"],
                "output_format"
            )
            args.extend(["--output-format", params["output_format"]])
            
        if params.get("system_prompt"):
            args.extend(["--system-prompt", params["system_prompt"]])
            
        if params.get("append_system_prompt"):
            args.extend(["--append-system-prompt", params["append_system_prompt"]])
            
        if params.get("continue_session"):
            args.append("--continue")
            
        if params.get("resume"):
            args.extend(["--resume", params["resume"]])
            
        if params.get("allowed_tools"):
            if isinstance(params["allowed_tools"], list):
                args.extend(["--allowedTools", ",".join(params["allowed_tools"])])
            else:
                args.extend(["--allowedTools", params["allowed_tools"]])
            
        if params.get("disallowed_tools"):
            if isinstance(params["disallowed_tools"], list):
                args.extend(["--disallowedTools", ",".join(params["disallowed_tools"])])
            else:
                args.extend(["--disallowedTools", params["disallowed_tools"]])
            
        if params.get("mcp_config"):
            args.extend(["--mcp-config", params["mcp_config"]])
            
        if params.get("max_turns") is not None:
            args.extend(["--max-turns", str(params["max_turns"])])
            
        if params.get("max_tokens") is not None:
            args.extend(["--max-tokens", str(params["max_tokens"])])
            
        if params.get("temperature") is not None:
            args.extend(["--temperature", str(params["temperature"])])
            
        if params.get("top_p") is not None:
            args.extend(["--top-p", str(params["top_p"])])
            
        if params.get("stop"):
            if isinstance(params["stop"], list):
                args.extend(["--stop", ",".join(params["stop"])])
            else:
                args.extend(["--stop", params["stop"]])
                
        # Add any additional parameters provided
        for key, value in params.items():
            if key not in [
                "prompt", "output_format", "system_prompt", "append_system_prompt",
                "continue_session", "resume", "allowed_tools", "disallowed_tools", 
                "mcp_config", "max_turns", "max_tokens", "temperature", "top_p", "stop"
            ] and value is not None:
                # Convert camelCase to kebab-case
                kebab_key = "".join(["-" + c.lower() if c.isupper() else c for c in key]).lstrip("-")
                args.extend([f"--{kebab_key}", str(value)])
                
        return args
    
    def _parse_error(self, stderr: str, returncode: int) -> ClaudeCodeError:
        """
        Parse error message from stderr
        
        Args:
            stderr: Standard error output
            returncode: Process return code
            
        Returns:
            ClaudeCodeError: Appropriate exception
        """
        # Try to parse JSON error
        try:
            error_data = json.loads(stderr)
            message = error_data.get("message", stderr)
            status = error_data.get("status", returncode or 500)
            code = error_data.get("code")
            param = error_data.get("param")
            request_id = error_data.get("request_id")
            
            return map_error_code_to_exception(
                status, message, code, param=param, request_id=request_id
            )
        except json.JSONDecodeError:
            # Handle common error patterns
            if "API key" in stderr or "authentication" in stderr.lower():
                return AuthenticationError(stderr)
            elif "rate limit" in stderr.lower() or "too many requests" in stderr.lower():
                return RateLimitError(stderr)
            elif "timed out" in stderr.lower() or "timeout" in stderr.lower():
                return TimeoutError(stderr)
            elif "invalid" in stderr.lower() or "missing" in stderr.lower():
                return InvalidRequestError(stderr)
            else:
                return APIError(stderr, status=returncode or 500)
    
    def execute(self, params: Dict[str, Any], timeout: Optional[int] = None) -> str:
        """
        Execute a Claude CLI command and return the result
        
        Args:
            params: Command parameters
            timeout: Command timeout in milliseconds
            
        Returns:
            str: Command output
            
        Raises:
            ClaudeCodeError: If command execution fails
        """
        # Use retry logic for transient errors
        def _execute_with_retry() -> str:
            args = self._build_args(params)
            timeout_seconds = (timeout or self.default_timeout) / 1000  # Convert to seconds
            
            logger.debug(f"Executing Claude CLI command: {self.cli_path} {' '.join(args)}")
            
            try:
                # Use subprocess.run for better control
                result = subprocess.run(
                    [self.cli_path, *args],
                    env=self.env,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds
                )
                
                if result.returncode != 0:
                    error = self._parse_error(result.stderr, result.returncode)
                    logger.error(f"Claude CLI error: {error}")
                    raise error
                    
                return result.stdout
                
            except subprocess.TimeoutExpired:
                error = TimeoutError(f"Claude CLI execution timed out after {timeout_seconds} seconds")
                logger.error(f"Claude CLI timeout: {error}")
                raise error
                
            except Exception as e:
                if isinstance(e, ClaudeCodeError):
                    raise e
                    
                error = APIError(f"Claude CLI execution failed: {str(e)}")
                logger.error(f"Claude CLI error: {error}")
                raise error
        
        return retry_with_backoff(
            _execute_with_retry,
            max_retries=self.max_retries,
            retry_codes=self.retry_codes
        )
    
    def execute_stream(self, params: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Execute a Claude CLI command in streaming mode
        
        Args:
            params: Command parameters
            
        Returns:
            Generator: Stream of response chunks
            
        Raises:
            ClaudeCodeError: If command execution fails
        """
        # Ensure we use stream-json format for streaming
        stream_params = {**params, "output_format": "stream-json"}
        args = self._build_args(stream_params)
        
        logger.debug(f"Executing Claude CLI stream command: {self.cli_path} {' '.join(args)}")
        
        # Start the process
        try:
            process = subprocess.Popen(
                [self.cli_path, *args],
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
        except FileNotFoundError:
            error = APIError(
                f"Claude CLI not found at path: {self.cli_path}. "
                "Please install it with: npm install -g @anthropic-ai/claude-code"
            )
            logger.error(f"Claude CLI error: {error}")
            raise error
        except Exception as e:
            error = APIError(f"Failed to start Claude CLI process: {str(e)}")
            logger.error(f"Claude CLI error: {error}")
            raise error
        
        # Read output line by line
        stderr_lines = []
        
        try:
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Parse JSON chunk
                    chunk = json.loads(line)
                    yield chunk
                except json.JSONDecodeError:
                    # Skip invalid JSON
                    logger.warning(f"Invalid JSON in stream: {line}")
                    continue
        except Exception as e:
            error = APIError(f"Error reading from Claude CLI stream: {str(e)}")
            logger.error(f"Claude CLI stream error: {error}")
            raise error
        finally:
            # Collect any stderr output
            if process.stderr:
                for line in process.stderr:
                    stderr_lines.append(line)
                    
            # Check for errors
            returncode = process.wait()
            if returncode != 0:
                stderr = "".join(stderr_lines)
                error = self._parse_error(stderr, returncode)
                logger.error(f"Claude CLI stream error: {error}")
                raise error