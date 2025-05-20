"""
Main client for Claude Code SDK
"""

from claude_code_sdk.client.base import BaseClient
from claude_code_sdk.client.chat import ChatCompletions
from claude_code_sdk.client.messages import Messages
from claude_code_sdk.client.sessions import Sessions
from claude_code_sdk.client.tools import Tools
from claude_code_sdk.types import ClaudeCodeOptions


class ClaudeCode(BaseClient):
    """Main client for Claude Code SDK"""
    
    def __init__(self, options: ClaudeCodeOptions = None):
        """
        Initialize the Claude Code client
        
        Args:
            options: Configuration options
        """
        super().__init__(options)
        
        # Initialize API components
        self.chat = self._init_chat()
        self.messages = Messages(self)
        self.sessions = Sessions(self)
        self.tools = Tools(self)
        
    def _init_chat(self):
        """Initialize chat completions with OpenAI-style interface"""
        completions = ChatCompletions(self)
        return {
            "completions": completions
        }