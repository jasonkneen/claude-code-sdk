"""
Chat completions API (OpenAI-style)
"""

from typing import Dict, List, Any, Optional, AsyncIterable, Union

from claude_code_sdk.client.base import BaseClient
from claude_code_sdk.implementations.converters import (
    convert_messages_to_prompt,
    parse_cli_output,
    convert_openai_to_anthropic_tools,
)


class ChatCompletions:
    """OpenAI-style chat completions API"""
    
    def __init__(self, client: BaseClient):
        """
        Initialize chat completions
        
        Args:
            client: Base client instance
        """
        self.client = client
        
    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a completion (OpenAI style)
        
        Args:
            params: OpenAI-style parameters
            
        Returns:
            Dict: OpenAI-style completion response
        """
        # Convert the OpenAI-style parameters to CLI parameters
        prompt = convert_messages_to_prompt(params["messages"])
        
        cli_params = {
            "prompt": prompt,
            "output_format": "json",
            "temperature": params.get("temperature"),
            "max_tokens": params.get("max_tokens"),
            "top_p": params.get("top_p"),
            "stop": params.get("stop"),
            "timeout": params.get("timeout"),
        }
        
        # Remove None values
        cli_params = {k: v for k, v in cli_params.items() if v is not None}
        
        # Handle stop sequences
        if "stop" in cli_params and isinstance(cli_params["stop"], list):
            cli_params["stop"] = ",".join(cli_params["stop"])
        
        # Handle tools if provided
        if "tools" in params and params["tools"]:
            anthropic_tools = convert_openai_to_anthropic_tools(params["tools"])
            tool_names = [tool["name"] for tool in anthropic_tools]
            cli_params["allowed_tools"] = tool_names
            
        if params.get("stream"):
            # Create streaming response
            return self.create_stream(params)
        else:
            # Execute and parse response
            output = self.client.execute_command(cli_params)
            return parse_cli_output(output)
    
    def create_stream(self, params: Dict[str, Any]) -> AsyncIterable[Dict[str, Any]]:
        """
        Create a streaming completion (OpenAI style)
        
        Args:
            params: OpenAI-style parameters
            
        Returns:
            AsyncIterable: Stream of completion chunks
        """
        # Convert the OpenAI-style parameters to CLI parameters
        prompt = convert_messages_to_prompt(params["messages"])
        
        cli_params = {
            "prompt": prompt,
            "output_format": "stream-json",
            "temperature": params.get("temperature"),
            "max_tokens": params.get("max_tokens"),
            "top_p": params.get("top_p"),
            "stop": params.get("stop"),
            "timeout": params.get("timeout"),
        }
        
        # Remove None values
        cli_params = {k: v for k, v in cli_params.items() if v is not None}
        
        # Handle stop sequences
        if "stop" in cli_params and isinstance(cli_params["stop"], list):
            cli_params["stop"] = ",".join(cli_params["stop"])
        
        # Handle tools if provided
        if "tools" in params and params["tools"]:
            anthropic_tools = convert_openai_to_anthropic_tools(params["tools"])
            tool_names = [tool["name"] for tool in anthropic_tools]
            cli_params["allowed_tools"] = tool_names
            
        # Get streaming response
        return self.client.execute_stream_command(cli_params)
    
    async def batch_create(self, params_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch create completions (custom extension)
        
        Args:
            params_list: List of OpenAI-style parameters
            
        Returns:
            List[Dict]: List of completion responses
        """
        results = []
        for params in params_list:
            results.append(self.create(params))
        return results