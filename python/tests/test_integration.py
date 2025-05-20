"""
Integration tests for Claude Code SDK
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from claude_code_sdk import ClaudeCode


# Skip these tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY environment variable not set"
)


class TestIntegration:
    """Integration tests for Claude Code SDK"""
    
    @patch("claude_code_sdk.implementations.cli.ClaudeCliExecutor.execute")
    def test_openai_style_completion(self, mock_execute):
        """Test OpenAI-style completion"""
        # Mock the CLI response
        mock_execute.return_value = '''
        {
            "id": "test-id",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello, I'm Claude!"
                    }
                }
            ],
            "session_id": "session123"
        }
        '''
        
        claude = ClaudeCode()
        response = claude.chat["completions"].create({
            "model": "claude-code",
            "messages": [
                {"role": "user", "content": "Hello, who are you?"}
            ]
        })
        
        assert response["id"] == "test-id"
        assert response["choices"][0]["message"]["role"] == "assistant"
        assert response["choices"][0]["message"]["content"] == "Hello, I'm Claude!"
        assert response["session_id"] == "session123"
        
    @patch("claude_code_sdk.implementations.cli.ClaudeCliExecutor.execute")
    def test_anthropic_style_completion(self, mock_execute):
        """Test Anthropic-style completion"""
        # Mock the CLI response
        mock_execute.return_value = '''
        {
            "id": "test-id",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, I'm Claude!"
                }
            ],
            "session_id": "session123"
        }
        '''
        
        claude = ClaudeCode()
        response = claude.messages.create({
            "model": "claude-code",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Hello, who are you?"}
                    ]
                }
            ]
        })
        
        assert "choices" in response
        assert response["choices"][0]["message"]["content"] == "Hello, I'm Claude!"
        
    @patch("claude_code_sdk.implementations.cli.ClaudeCliExecutor.execute")
    def test_session_management(self, mock_execute):
        """Test session management"""
        # Mock the CLI response for session creation
        mock_execute.return_value = '''
        {
            "id": "test-id",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello, I'm Claude!"
                    }
                }
            ],
            "session_id": "session123"
        }
        '''
        
        claude = ClaudeCode()
        session = claude.sessions.create({
            "messages": [
                {"role": "user", "content": "Hello, who are you?"}
            ]
        })
        
        assert session.id == "session123"
        
        # Mock the CLI response for session continuation
        mock_execute.return_value = '''
        {
            "id": "test-id-2",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I'm doing well, thank you!"
                    }
                }
            ],
            "session_id": "session123"
        }
        '''
        
        response = session.continue_session({
            "messages": [
                {"role": "user", "content": "How are you?"}
            ]
        })
        
        assert response["id"] == "test-id-2"
        assert response["choices"][0]["message"]["content"] == "I'm doing well, thank you!"
        
    def test_tool_management(self):
        """Test tool management"""
        claude = ClaudeCode()
        
        # Create a tool
        tool = claude.tools.create({
            "name": "calculator",
            "description": "Perform calculations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        })
        
        assert tool["name"] == "calculator"
        
        # Get the tool
        retrieved_tool = claude.tools.get("calculator")
        assert retrieved_tool["name"] == "calculator"
        assert retrieved_tool["description"] == "Perform calculations"
        
        # List tools
        tools = claude.tools.list()
        assert len(tools) == 1
        assert tools[0]["name"] == "calculator"
        
        # Delete the tool
        result = claude.tools.delete("calculator")
        assert result is True
        
        # Verify it's gone
        assert claude.tools.get("calculator") is None