"""
Logging configuration for Claude Code SDK
"""

import logging
import os
from typing import Optional, Dict, Any, Union

# Configure logging
logger = logging.getLogger("claude_code_sdk")


def configure_logging(
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
) -> None:
    """
    Configure logging for Claude Code SDK
    
    Args:
        level: Logging level (default: INFO)
        format_string: Log format string
        log_file: Optional file path to write logs
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
    formatter = logging.Formatter(format_string)
    
    # Configure root logger
    root_logger = logging.getLogger("claude_code_sdk")
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set default level from environment variable if present
    env_level = os.environ.get("CLAUDE_CODE_LOG_LEVEL")
    if env_level:
        try:
            numeric_level = getattr(logging, env_level.upper(), None)
            if isinstance(numeric_level, int):
                root_logger.setLevel(numeric_level)
        except (AttributeError, TypeError):
            pass