"""
Tests for the CLI executor
"""

import pytest
import json
import subprocess
from unittest.mock import patch, MagicMock

from claude_code_sdk.implementations.cli import ClaudeCliExecutor


class TestClaudeCliExecutor:
    """Test suite for ClaudeCliExecutor"""
    
    def test_init(self):
        """Test initialization with default values"""
        executor = ClaudeCliExecutor()
        assert executor.cli_path == "@anthropic-ai/claude-code"
        assert executor.default_timeout == 300000
        
    def test_init_with_options(self):
        """Test initialization with custom options"""
        executor = ClaudeCliExecutor(
            cli_path="custom-path",
            timeout=60000,
            env={"CUSTOM_VAR": "value"}
        )
        assert executor.cli_path == "custom-path"
        assert executor.default_timeout == 60000
        assert "CUSTOM_VAR" in executor.env
        assert executor.env["CUSTOM_VAR"] == "value"
        
    def test_build_args(self):
        """Test building command line arguments"""
        executor = ClaudeCliExecutor()
        params = {
            "prompt": "Test prompt",
            "output_format": "json",
            "system_prompt": "You are a helpful assistant",
            "continue_session": True,
            "resume": "session-id",
            "allowed_tools": ["tool1", "tool2"],
            "max_turns": 5,
            "temperature": 0.7
        }
        
        args = executor._build_args(params)
        
        assert "-p" in args
        assert "Test prompt" in args
        assert "--output-format" in args
        assert "json" in args
        assert "--system-prompt" in args
        assert "You are a helpful assistant" in args
        assert "--continue" in args
        assert "--resume" in args
        assert "session-id" in args
        assert "--allowedTools" in args
        assert "tool1,tool2" in args
        assert "--max-turns" in args
        assert "5" in args
        assert "--temperature" in args
        assert "0.7" in args
        
    @patch("subprocess.run")
    def test_execute_success(self, mock_run):
        """Test successful command execution"""
        # Mock the subprocess.run return value
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = '{"result": "success"}'
        mock_run.return_value = mock_process
        
        executor = ClaudeCliExecutor()
        result = executor.execute({"prompt": "Test"})
        
        assert result == '{"result": "success"}'
        mock_run.assert_called_once()
        
    @patch("subprocess.run")
    def test_execute_error(self, mock_run):
        """Test command execution with error"""
        # Mock the subprocess.run return value
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "Command failed"
        mock_run.return_value = mock_process
        
        executor = ClaudeCliExecutor()
        
        with pytest.raises(Exception) as excinfo:
            executor.execute({"prompt": "Test"})
            
        assert "exited with code 1" in str(excinfo.value)
        assert hasattr(excinfo.value, "status")
        assert excinfo.value.status == 1
        
    @patch("subprocess.run")
    def test_execute_timeout(self, mock_run):
        """Test command execution with timeout"""
        # Mock the subprocess.run to raise TimeoutExpired
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=5)
        
        executor = ClaudeCliExecutor()
        
        with pytest.raises(Exception) as excinfo:
            executor.execute({"prompt": "Test"})
            
        assert "timed out" in str(excinfo.value)
        assert hasattr(excinfo.value, "status")
        assert excinfo.value.status == 408
        
    @patch("subprocess.Popen")
    def test_execute_stream(self, mock_popen):
        """Test streaming command execution"""
        # Mock the subprocess.Popen
        mock_process = MagicMock()
        mock_process.stdout = [
            '{"type": "assistant", "content": "Hello"}',
            '{"type": "assistant", "content": "World"}'
        ]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        executor = ClaudeCliExecutor()
        stream = executor.execute_stream({"prompt": "Test"})
        
        chunks = list(stream)
        assert len(chunks) == 2
        assert chunks[0]["type"] == "assistant"
        assert chunks[0]["content"] == "Hello"
        assert chunks[1]["type"] == "assistant"
        assert chunks[1]["content"] == "World"