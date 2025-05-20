"""
Exception handling for Claude Code SDK
"""

from typing import Optional, Dict, Any, List


class ClaudeCodeError(Exception):
    """Base exception for Claude Code SDK"""
    
    def __init__(
        self, 
        message: str, 
        status: int = 500, 
        code: Optional[str] = None,
        param: Optional[str] = None,
        request_id: Optional[str] = None
    ):
        """
        Initialize a Claude Code error
        
        Args:
            message: Error message
            status: HTTP status code
            code: Error code
            param: Parameter that caused the error
            request_id: Request ID for tracking
        """
        super().__init__(message)
        self.status = status
        self.code = code
        self.param = param
        self.request_id = request_id
        
    def __str__(self) -> str:
        """String representation of the error"""
        parts = [super().__str__()]
        
        if self.code:
            parts.append(f"Code: {self.code}")
        
        if self.status:
            parts.append(f"Status: {self.status}")
            
        if self.param:
            parts.append(f"Parameter: {self.param}")
            
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}")
            
        return " | ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        return {
            "message": str(self),
            "status": self.status,
            "code": self.code,
            "param": self.param,
            "request_id": self.request_id
        }


class AuthenticationError(ClaudeCodeError):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status=401, code="authentication_error", **kwargs)


class RateLimitError(ClaudeCodeError):
    """Rate limit error"""
    
    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        super().__init__(message, status=429, code="rate_limit_error", **kwargs)


class APIError(ClaudeCodeError):
    """API error"""
    
    def __init__(self, message: str = "API error", **kwargs):
        super().__init__(message, status=500, code="api_error", **kwargs)


class InvalidRequestError(ClaudeCodeError):
    """Invalid request error"""
    
    def __init__(self, message: str = "Invalid request", **kwargs):
        super().__init__(message, status=400, code="invalid_request", **kwargs)


class TimeoutError(ClaudeCodeError):
    """Timeout error"""
    
    def __init__(self, message: str = "Request timed out", **kwargs):
        super().__init__(message, status=408, code="timeout_error", **kwargs)


class ToolError(ClaudeCodeError):
    """Tool error"""
    
    def __init__(self, message: str = "Tool execution failed", **kwargs):
        super().__init__(message, status=500, code="tool_error", **kwargs)


def map_error_code_to_exception(
    status: int, 
    message: str, 
    code: Optional[str] = None,
    **kwargs
) -> ClaudeCodeError:
    """
    Map error code to appropriate exception
    
    Args:
        status: HTTP status code
        message: Error message
        code: Error code
        **kwargs: Additional error parameters
        
    Returns:
        ClaudeCodeError: Appropriate exception instance
    """
    if status == 401:
        return AuthenticationError(message, **kwargs)
    elif status == 429:
        return RateLimitError(message, **kwargs)
    elif status == 400:
        return InvalidRequestError(message, **kwargs)
    elif status == 408:
        return TimeoutError(message, **kwargs)
    else:
        return APIError(message, status=status, code=code, **kwargs)