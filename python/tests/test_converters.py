"""
Tests for the converters
"""

import pytest
import json
from claude_code_sdk.implementations.converters import (
    convert_messages_to_prompt,
    convert_anthropic_messages_to_prompt,
    parse_cli_output,
    convert_openai_to_anthropic_tools,
    convert_anthropic_to_openai_response
)


class TestConverters:
    """Test suite for converter functions"""
    
    def test_convert_messages_to_prompt(self):
        """Test converting OpenAI-style messages to prompt"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
            {"role": "user", "content": "How are you?"}
        ]
        
        prompt = convert_messages_to_prompt(messages)
        
        # System messages should be skipped
        assert "You are a helpful assistant" not in prompt
        
        # User and assistant messages should be included
        assert "User: Hello" in prompt
        assert "Assistant: Hi there" in prompt
        assert "User: How are you?" in prompt
        
    def test_convert_anthropic_messages_to_prompt(self):
        """Test converting Anthropic-style messages to prompt"""
        # Test with string content
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        
        prompt = convert_anthropic_messages_to_prompt(messages)
        
        # System messages should be skipped
        assert "You are a helpful assistant" not in prompt
        
        # User and assistant messages should be included
        assert "User: Hello" in prompt
        assert "Assistant: Hi there" in prompt
        
        # Test with content blocks
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": "Hello"}
            ]},
            {"role": "assistant", "content": [
                {"type": "text", "text": "Hi there"}
            ]}
        ]
        
        prompt = convert_anthropic_messages_to_prompt(messages)
        
        assert "User: Hello" in prompt
        assert "Assistant: Hi there" in prompt
        
    def test_parse_cli_output(self):
        """Test parsing CLI output"""
        # Test with valid JSON
        output = '{"id": "test", "choices": [{"message": {"content": "Hello"}}]}'
        result = parse_cli_output(output)
        
        assert result["id"] == "test"
        assert result["choices"][0]["message"]["content"] == "Hello"
        
        # Test with non-JSON output
        output = "Plain text response"
        result = parse_cli_output(output)
        
        assert "choices" in result
        assert result["choices"][0]["message"]["role"] == "assistant"
        assert result["choices"][0]["message"]["content"] == "Plain text response"
        
    def test_convert_openai_to_anthropic_tools(self):
        """Test converting OpenAI tools to Anthropic format"""
        openai_tools = [
            {
                "name": "calculator",
                "description": "Perform calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"}
                    }
                }
            }
        ]
        
        anthropic_tools = convert_openai_to_anthropic_tools(openai_tools)
        
        assert len(anthropic_tools) == 1
        assert anthropic_tools[0]["name"] == "calculator"
        assert anthropic_tools[0]["description"] == "Perform calculations"
        assert "input_schema" in anthropic_tools[0]
        assert anthropic_tools[0]["input_schema"]["properties"]["expression"]["type"] == "string"
        
    def test_convert_anthropic_to_openai_response(self):
        """Test converting Anthropic response to OpenAI format"""
        # Test with already OpenAI format
        openai_response = {
            "id": "test",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello"
                    }
                }
            ]
        }
        
        result = convert_anthropic_to_openai_response(openai_response)
        assert result == openai_response
        
        # Test with Anthropic format
        anthropic_response = {
            "id": "test",
            "content": [
                {"type": "text", "text": "Hello world"}
            ],
            "session_id": "session123"
        }
        
        result = convert_anthropic_to_openai_response(anthropic_response)
        
        assert result["id"] == "test"
        assert result["session_id"] == "session123"
        assert result["choices"][0]["message"]["role"] == "assistant"
        assert result["choices"][0]["message"]["content"] == "Hello world"