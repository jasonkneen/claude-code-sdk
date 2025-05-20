"""
Tests for the client classes
"""

import pytest
from unittest.mock import patch, MagicMock

from claude_code_sdk import ClaudeCode
from claude_code_sdk.client.base import BaseClient
from claude_code_sdk.client.chat import ChatCompletions
from claude_code_sdk.client.messages import Messages
from claude_code_sdk.client.sessions import Sessions, Session
from claude_code_sdk.client.tools import Tools


class TestBaseClient:
    """Test suite for BaseClient"""
    
    def test_init(self):
        """Test initialization with default values"""
        client = BaseClient()
        assert client.default_model == "claude-code"
        assert client.default_timeout == 300000
        assert client.executor is not None
        
    def test_init_with_options(self):
        """Test initialization with custom options"""
        client = BaseClient({
            "api_key": "test-key",
            "cli_path": "custom-path",
            "timeout": 60000
        })
        assert client.api_key == "test-key"
        assert client.default_timeout == 60000
        assert client.executor.cli_path == "custom-path"
        
    def test_create_error(self):
        """Test error creation"""
        client = BaseClient()
        error = client.create_error("Test error", 404, "not_found")
        
        assert str(error) == "Test error"
        assert error.status == 404
        assert error.code == "not_found"
        
    @patch("claude_code_sdk.implementations.cli.ClaudeCliExecutor.execute")
    def test_execute_command(self, mock_execute):
        """Test command execution"""
        mock_execute.return_value = '{"result": "success"}'
        
        client = BaseClient()
        result = client.execute_command({"prompt": "Test"})
        
        assert result == '{"result": "success"}'
        mock_execute.assert_called_once()
        
    @patch("claude_code_sdk.implementations.cli.ClaudeCliExecutor.execute")
    def test_execute_command_error(self, mock_execute):
        """Test command execution with error"""
        error = Exception("Command failed")
        setattr(error, "status", 500)
        mock_execute.side_effect = error
        
        client = BaseClient()
        
        with pytest.raises(Exception) as excinfo:
            client.execute_command({"prompt": "Test"})
            
        assert "Command failed" in str(excinfo.value)
        assert hasattr(excinfo.value, "status")
        assert excinfo.value.status == 500


class TestClaudeCode:
    """Test suite for ClaudeCode main client"""
    
    def test_init(self):
        """Test initialization"""
        client = ClaudeCode()
        
        assert client.chat is not None
        assert "completions" in client.chat
        assert client.messages is not None
        assert client.sessions is not None
        assert client.tools is not None
        
    def test_init_with_options(self):
        """Test initialization with options"""
        client = ClaudeCode({
            "api_key": "test-key",
            "cli_path": "custom-path",
            "timeout": 60000
        })
        
        assert client.api_key == "test-key"
        assert client.default_timeout == 60000


class TestChatCompletions:
    """Test suite for ChatCompletions"""
    
    @patch("claude_code_sdk.client.base.BaseClient.execute_command")
    def test_create(self, mock_execute):
        """Test create completion"""
        mock_execute.return_value = '{"id": "test", "choices": [{"message": {"content": "Hello"}}]}'
        
        client = BaseClient()
        chat = ChatCompletions(client)
        
        result = chat.create({
            "model": "claude-code",
            "messages": [{"role": "user", "content": "Hello"}]
        })
        
        assert result["id"] == "test"
        assert result["choices"][0]["message"]["content"] == "Hello"
        mock_execute.assert_called_once()
        
    @patch("claude_code_sdk.client.base.BaseClient.execute_stream_command")
    def test_create_stream(self, mock_stream):
        """Test create streaming completion"""
        mock_stream.return_value = [
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": " world"}}]}
        ]
        
        client = BaseClient()
        chat = ChatCompletions(client)
        
        stream = chat.create_stream({
            "model": "claude-code",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": True
        })
        
        assert mock_stream.called
        
    @patch("claude_code_sdk.client.chat.ChatCompletions.create")
    def test_create_with_tools(self, mock_create):
        """Test create with tools"""
        mock_create.return_value = {"id": "test"}
        
        client = BaseClient()
        chat = ChatCompletions(client)
        
        result = chat.create({
            "model": "claude-code",
            "messages": [{"role": "user", "content": "Hello"}],
            "tools": [
                {
                    "name": "calculator",
                    "description": "Calculate expressions",
                    "parameters": {"type": "object"}
                }
            ]
        })
        
        assert result["id"] == "test"
        mock_create.assert_called_once()


class TestMessages:
    """Test suite for Messages"""
    
    @patch("claude_code_sdk.client.base.BaseClient.execute_command")
    def test_create(self, mock_execute):
        """Test create message"""
        mock_execute.return_value = '{"id": "test", "choices": [{"message": {"content": "Hello"}}]}'
        
        client = BaseClient()
        messages = Messages(client)
        
        result = messages.create({
            "model": "claude-code",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": "Hello"}]
                }
            ]
        })
        
        assert "choices" in result
        mock_execute.assert_called_once()
        
    @patch("claude_code_sdk.client.base.BaseClient.execute_stream_command")
    def test_create_stream(self, mock_stream):
        """Test create streaming message"""
        mock_stream.return_value = [
            {"type": "content_block_delta", "delta": {"text": "Hello"}},
            {"type": "content_block_delta", "delta": {"text": " world"}}
        ]
        
        client = BaseClient()
        messages = Messages(client)
        
        stream = messages.create_stream({
            "model": "claude-code",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": "Hello"}]
                }
            ],
            "stream": True
        })
        
        assert mock_stream.called


class TestSessions:
    """Test suite for Sessions"""
    
    @patch("claude_code_sdk.client.chat.ChatCompletions.create")
    def test_create(self, mock_create):
        """Test create session"""
        mock_create.return_value = {"id": "test", "session_id": "session123"}
        
        client = BaseClient()
        sessions = Sessions(client)
        
        session = sessions.create({
            "messages": [{"role": "user", "content": "Hello"}]
        })
        
        assert isinstance(session, Session)
        assert session.id == "session123"
        mock_create.assert_called_once()
        
    def test_resume(self):
        """Test resume session"""
        client = BaseClient()
        sessions = Sessions(client)
        
        session = sessions.resume("session123")
        
        assert isinstance(session, Session)
        assert session.id == "session123"


class TestSession:
    """Test suite for Session"""
    
    @patch("claude_code_sdk.client.chat.ChatCompletions.create")
    def test_continue_session(self, mock_create):
        """Test continue session"""
        mock_create.return_value = {"id": "test", "choices": [{"message": {"content": "Hello"}}]}
        
        client = BaseClient()
        session = Session(client, "session123")
        
        result = session.continue_session({
            "messages": [{"role": "user", "content": "Hello"}]
        })
        
        assert result["id"] == "test"
        mock_create.assert_called_once()
        
        # Check that resume parameter was added
        args = mock_create.call_args[0][0]
        assert args["resume"] == "session123"
        
    @patch("claude_code_sdk.client.chat.ChatCompletions.create_stream")
    def test_continue_stream(self, mock_stream):
        """Test continue session with streaming"""
        mock_stream.return_value = [
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": " world"}}]}
        ]
        
        client = BaseClient()
        session = Session(client, "session123")
        
        stream = session.continue_stream({
            "messages": [{"role": "user", "content": "Hello"}]
        })
        
        assert mock_stream.called
        
        # Check that resume parameter was added
        args = mock_stream.call_args[0][0]
        assert args["resume"] == "session123"
        assert args["stream"] == True


class TestTools:
    """Test suite for Tools"""
    
    def test_create(self):
        """Test create tool"""
        client = BaseClient()
        tools = Tools(client)
        
        tool = tools.create({
            "name": "calculator",
            "description": "Perform calculations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                }
            }
        })
        
        assert tool["name"] == "calculator"
        assert tool["description"] == "Perform calculations"
        
    def test_get(self):
        """Test get tool"""
        client = BaseClient()
        tools = Tools(client)
        
        tools.create({
            "name": "calculator",
            "description": "Perform calculations"
        })
        
        tool = tools.get("calculator")
        
        assert tool is not None
        assert tool["name"] == "calculator"
        
        # Test non-existent tool
        tool = tools.get("non-existent")
        assert tool is None
        
    def test_list(self):
        """Test list tools"""
        client = BaseClient()
        tools = Tools(client)
        
        tools.create({"name": "tool1"})
        tools.create({"name": "tool2"})
        
        tool_list = tools.list()
        
        assert len(tool_list) == 2
        assert tool_list[0]["name"] == "tool1"
        assert tool_list[1]["name"] == "tool2"
        
    def test_delete(self):
        """Test delete tool"""
        client = BaseClient()
        tools = Tools(client)
        
        tools.create({"name": "tool1"})
        
        # Delete existing tool
        result = tools.delete("tool1")
        assert result is True
        assert tools.get("tool1") is None
        
        # Delete non-existent tool
        result = tools.delete("non-existent")
        assert result is False