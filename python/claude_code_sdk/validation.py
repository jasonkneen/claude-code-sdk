"""
Validation utilities for Claude Code SDK
"""

import re
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, cast

from claude_code_sdk.exceptions import InvalidRequestError

T = TypeVar('T')


def validate_required(
    params: Dict[str, Any],
    required_fields: List[str],
    error_prefix: str = "Missing required parameter"
) -> None:
    """
    Validate required fields in parameters
    
    Args:
        params: Parameters to validate
        required_fields: List of required field names
        error_prefix: Prefix for error messages
        
    Raises:
        InvalidRequestError: If a required field is missing
    """
    for field in required_fields:
        if field not in params or params[field] is None:
            raise InvalidRequestError(
                f"{error_prefix}: {field}",
                param=field
            )


def validate_type(
    value: Any,
    expected_type: Union[type, List[type]],
    param_name: str,
    allow_none: bool = False
) -> None:
    """
    Validate parameter type
    
    Args:
        value: Value to validate
        expected_type: Expected type or list of types
        param_name: Parameter name for error messages
        allow_none: Whether None is allowed
        
    Raises:
        InvalidRequestError: If value is not of expected type
    """
    if value is None:
        if allow_none:
            return
        raise InvalidRequestError(
            f"Parameter '{param_name}' cannot be None",
            param=param_name
        )
        
    if isinstance(expected_type, list):
        if not any(isinstance(value, t) for t in expected_type):
            type_names = [t.__name__ for t in expected_type]
            raise InvalidRequestError(
                f"Parameter '{param_name}' must be one of types: {', '.join(type_names)}",
                param=param_name
            )
    elif not isinstance(value, expected_type):
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be of type {expected_type.__name__}",
            param=param_name
        )


def validate_range(
    value: Union[int, float],
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None,
    param_name: str = "value"
) -> None:
    """
    Validate numeric value is within range
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        param_name: Parameter name for error messages
        
    Raises:
        InvalidRequestError: If value is outside allowed range
    """
    if min_value is not None and value < min_value:
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be greater than or equal to {min_value}",
            param=param_name
        )
        
    if max_value is not None and value > max_value:
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be less than or equal to {max_value}",
            param=param_name
        )


def validate_string_length(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    param_name: str = "value"
) -> None:
    """
    Validate string length is within range
    
    Args:
        value: String to validate
        min_length: Minimum allowed length (inclusive)
        max_length: Maximum allowed length (inclusive)
        param_name: Parameter name for error messages
        
    Raises:
        InvalidRequestError: If string length is outside allowed range
    """
    if min_length is not None and len(value) < min_length:
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be at least {min_length} characters long",
            param=param_name
        )
        
    if max_length is not None and len(value) > max_length:
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be at most {max_length} characters long",
            param=param_name
        )


def validate_pattern(
    value: str,
    pattern: str,
    param_name: str = "value",
    error_message: Optional[str] = None
) -> None:
    """
    Validate string matches regex pattern
    
    Args:
        value: String to validate
        pattern: Regex pattern to match
        param_name: Parameter name for error messages
        error_message: Custom error message
        
    Raises:
        InvalidRequestError: If string doesn't match pattern
    """
    if not re.match(pattern, value):
        message = error_message or f"Parameter '{param_name}' must match pattern: {pattern}"
        raise InvalidRequestError(message, param=param_name)


def validate_enum(
    value: Any,
    allowed_values: List[Any],
    param_name: str = "value",
    case_sensitive: bool = True
) -> None:
    """
    Validate value is one of allowed values
    
    Args:
        value: Value to validate
        allowed_values: List of allowed values
        param_name: Parameter name for error messages
        case_sensitive: Whether string comparison is case-sensitive
        
    Raises:
        InvalidRequestError: If value is not in allowed values
    """
    if isinstance(value, str) and not case_sensitive:
        if not any(str(v).lower() == value.lower() for v in allowed_values):
            raise InvalidRequestError(
                f"Parameter '{param_name}' must be one of: {', '.join(str(v) for v in allowed_values)}",
                param=param_name
            )
    elif value not in allowed_values:
        raise InvalidRequestError(
            f"Parameter '{param_name}' must be one of: {', '.join(str(v) for v in allowed_values)}",
            param=param_name
        )


def validate_and_cast(
    value: Any,
    validator: Callable[[Any], bool],
    cast_func: Callable[[Any], T],
    param_name: str = "value",
    error_message: Optional[str] = None
) -> T:
    """
    Validate and cast value
    
    Args:
        value: Value to validate and cast
        validator: Function that returns True if value is valid
        cast_func: Function to cast value to desired type
        param_name: Parameter name for error messages
        error_message: Custom error message
        
    Returns:
        T: Cast value
        
    Raises:
        InvalidRequestError: If validation fails
    """
    if not validator(value):
        message = error_message or f"Parameter '{param_name}' failed validation"
        raise InvalidRequestError(message, param=param_name)
        
    try:
        return cast_func(value)
    except Exception as e:
        raise InvalidRequestError(
            f"Failed to cast parameter '{param_name}': {str(e)}",
            param=param_name
        )