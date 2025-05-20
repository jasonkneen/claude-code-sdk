"""
Rate limiting and retry logic for Claude Code SDK
"""

import time
import random
from typing import Callable, TypeVar, Any, Optional, Dict, List, Union
import logging

from claude_code_sdk.exceptions import RateLimitError, TimeoutError, APIError

# Configure logger
logger = logging.getLogger("claude_code_sdk.retry")

# Type variable for generic function
T = TypeVar('T')


def exponential_backoff(
    retry_count: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
) -> float:
    """
    Calculate exponential backoff delay
    
    Args:
        retry_count: Current retry attempt (0-based)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter
        
    Returns:
        float: Delay in seconds
    """
    delay = min(max_delay, base_delay * (2 ** retry_count))
    
    if jitter:
        # Add random jitter between 0-30%
        jitter_amount = random.uniform(0, 0.3)
        delay = delay * (1 + jitter_amount)
        
    return delay


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    retry_codes: Optional[List[int]] = None,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    *args: Any,
    **kwargs: Any
) -> T:
    """
    Retry a function with exponential backoff
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        retry_codes: HTTP status codes to retry on
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        T: Function result
        
    Raises:
        Exception: Last exception encountered
    """
    if retry_codes is None:
        # Default to retrying on rate limit and server errors
        retry_codes = [429, 500, 502, 503, 504]
        
    last_exception = None
    
    for retry in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            
            # Check if we should retry based on error type
            should_retry = False
            
            if isinstance(e, RateLimitError) or (hasattr(e, "status") and getattr(e, "status") in retry_codes):
                should_retry = True
            
            # Don't retry on timeout unless explicitly included in retry_codes
            if isinstance(e, TimeoutError) and 408 not in retry_codes:
                should_retry = False
                
            if retry >= max_retries or not should_retry:
                raise
                
            # Calculate backoff delay
            delay = exponential_backoff(retry, base_delay, max_delay, jitter)
            
            # Log retry attempt
            logger.warning(
                f"Retrying after error: {str(e)}. "
                f"Attempt {retry + 1}/{max_retries}. "
                f"Waiting {delay:.2f} seconds..."
            )
            
            # Wait before retrying
            time.sleep(delay)
    
    # This should never happen, but just in case
    if last_exception:
        raise last_exception
    
    # This should also never happen
    raise APIError("Unexpected error in retry logic")