"""
Converters for Claude Code SDK
"""

import json
from typing import Dict, List, Any, TypeVar, Generic, Optional, Union

T = TypeVar('T')


def convert_messages_to_prompt(messages: List[Dict[str, Any]]) -> str:
    """
    Convert OpenAI-style messages to a prompt string
    
    Args:
        messages: List of OpenAI-style messages
        
    Returns:
        str: Prompt string
    """
    prompt = ""
    
    for message in messages:
        role = message.get("role", "").lower()
        content = message.get("content", "")
        
        if role == "system":
            # System messages are handled separately via --system-prompt
            continue
        elif role == "user":
            prompt += f"User: {content}\n\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n\n"
        elif role == "tool":
            # Tool messages are handled differently
            name = message.get("name", "unknown")
            prompt += f"Tool ({name}): {content}\n\n"
            
    return prompt.strip()


def convert_anthropic_messages_to_prompt(messages: List[Dict[str, Any]]) -> str:
    """
    Convert Anthropic-style messages to a prompt string
    
    Args:
        messages: List of Anthropic-style messages
        
    Returns:
        str: Prompt string
    """
    prompt = ""
    
    for message in messages:
        role = message.get("role", "").lower()
        content = message.get("content", [])
        
        # Handle different content formats
        if isinstance(content, str):
            message_content = content
        elif isinstance(content, list):
            # Extract text from content blocks
            message_content = ""
            for block in content:
                if block.get("type") == "text":
                    message_content += block.get("text", "")
        else:
            message_content = str(content)
        
        if role == "system":
            # System messages are handled separately via --system-prompt
            continue
        elif role == "user":
            prompt += f"User: {message_content}\n\n"
        elif role == "assistant":
            prompt += f"Assistant: {message_content}\n\n"
            
    return prompt.strip()


def parse_cli_output(output: str) -> Dict[str, Any]:
    """
    Parse CLI output to a structured response
    
    Args:
        output: CLI output string
        
    Returns:
        Dict: Parsed response
    """
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # If not JSON, return as text
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": output
                    }
                }
            ]
        }


def convert_openai_to_anthropic_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert OpenAI-style tools to Anthropic format
    
    Args:
        tools: OpenAI-style tools
        
    Returns:
        List[Dict]: Anthropic-style tools
    """
    anthropic_tools = []
    
    for tool in tools:
        anthropic_tool = {
            "name": tool.get("name", ""),
            "description": tool.get("description", ""),
            "input_schema": tool.get("parameters", {})
        }
        anthropic_tools.append(anthropic_tool)
        
    return anthropic_tools


def convert_anthropic_to_openai_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Anthropic-style response to OpenAI format
    
    Args:
        response: Anthropic-style response
        
    Returns:
        Dict: OpenAI-style response
    """
    # If it's already in OpenAI format, return as is
    if "choices" in response:
        return response
        
    # Convert from Anthropic format
    content_blocks = response.get("content", [])
    content_text = ""
    
    for block in content_blocks:
        if block.get("type") == "text":
            content_text += block.get("text", "")
            
    return {
        "id": response.get("id", ""),
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": content_text
                }
            }
        ],
        "session_id": response.get("session_id", "")
    }