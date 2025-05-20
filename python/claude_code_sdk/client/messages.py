"""
Messages API (Anthropic-style)
"""

from typing import Dict, List, Any, Optional, AsyncIterable

from claude_code_sdk.client.base import BaseClient
from claude_code_sdk.implementations.converters import (
    convert_anthropic_messages_to_prompt,
    parse_cli_output,
    convert_anthropic_to_openai_response,
)


class Messages:
    """Anthropic-style messages API"""
    
    def __init__(self, client: BaseClient):
        """
        Initialize messages API
        
        Args:
            client: Base client instance
        """
        self.client = client
        
    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a message (Anthropic style)
        
        Args:
            params: Anthropic-style parameters
            
        Returns:
            Dict: Anthropic-style message response
        """
        # Convert the Anthropic-style parameters to CLI parameters
        prompt = convert_anthropic_messages_to_prompt(params["messages"])
        
        cli_params = {
            "prompt": prompt,
            "output_format": "json",
            "temperature": params.get("temperature"),
            "max_tokens": params.get("max_tokens"),
            "top_p": params.get("top_p"),
            "stop_sequences": params.get("stop_sequences"),
            "timeout": params.get("timeout"),
        }
        
        # Remove None values
        cli_params = {k: v for k, v in cli_params.items() if v is not None}
        
        # Handle stop sequences
        if "stop_sequences" in cli_params and isinstance(cli_params["stop_sequences"], list):
            cli_params["stop"] = ",".join(cli_params["stop_sequences"])
            del cli_params["stop_sequences"]
        
        # Handle tools if provided
        if "tools" in params and params["tools"]:
            tool_names = [tool["name"] for tool in params["tools"]]
            cli_params["allowed_tools"] = tool_names
            
        if params.get("stream"):
            # Create streaming response
            return self.create_stream(params)
        else:
            # Execute and parse response
            output = self.client.execute_command(cli_params)
            response = parse_cli_output(output)
            
            # Convert to Anthropic format if needed
            return convert_anthropic_to_openai_response(response)
    
    def create_stream(self, params: Dict[str, Any]) -> AsyncIterable[Dict[str, Any]]:
        """
        Create a streaming message (Anthropic style)
        
        Args:
            params: Anthropic-style parameters
            
        Returns:
            AsyncIterable: Stream of message chunks
        """
        # Convert the Anthropic-style parameters to CLI parameters
        prompt = convert_anthropic_messages_to_prompt(params["messages"])
        
        cli_params = {
            "prompt": prompt,
            "output_format": "stream-json",
            "temperature": params.get("temperature"),
            "max_tokens": params.get("max_tokens"),
            "top_p": params.get("top_p"),
            "stop_sequences": params.get("stop_sequences"),
            "timeout": params.get("timeout"),
        }
        
        # Remove None values
        cli_params = {k: v for k, v in cli_params.items() if v is not None}
        
        # Handle stop sequences
        if "stop_sequences" in cli_params and isinstance(cli_params["stop_sequences"], list):
            cli_params["stop"] = ",".join(cli_params["stop_sequences"])
            del cli_params["stop_sequences"]
        
        # Handle tools if provided
        if "tools" in params and params["tools"]:
            tool_names = [tool["name"] for tool in params["tools"]]
            cli_params["allowed_tools"] = tool_names
            
        # Get streaming response
        return self.client.execute_stream_command(cli_params)