"""
Session management for Claude Code SDK
"""

from typing import Dict, List, Any, Optional

from claude_code_sdk.client.base import BaseClient
from claude_code_sdk.client.chat import ChatCompletions


class Session:
    """Claude Code session"""
    
    def __init__(self, client: BaseClient, session_id: str):
        """
        Initialize a session
        
        Args:
            client: Base client instance
            session_id: Session ID
        """
        self.client = client
        self.id = session_id
        self.chat = ChatCompletions(client)
        
    def continue_session(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continue the session with new messages
        
        Args:
            params: Parameters for continuation
            
        Returns:
            Dict: Response from Claude
        """
        # Add session ID to parameters
        continue_params = params.copy()
        continue_params["resume"] = self.id
        
        # Use chat completions to handle the request
        return self.chat.create(continue_params)
    
    def continue_stream(self, params: Dict[str, Any]):
        """
        Continue the session with streaming
        
        Args:
            params: Parameters for continuation
            
        Returns:
            AsyncIterable: Stream of response chunks
        """
        # Add session ID to parameters
        continue_params = params.copy()
        continue_params["resume"] = self.id
        continue_params["stream"] = True
        
        # Use chat completions to handle the request
        return self.chat.create_stream(continue_params)


class Sessions:
    """Session management API"""
    
    def __init__(self, client: BaseClient):
        """
        Initialize sessions API
        
        Args:
            client: Base client instance
        """
        self.client = client
        self.chat = ChatCompletions(client)
        
    def create(self, params: Dict[str, Any]) -> Session:
        """
        Create a new session
        
        Args:
            params: Parameters for the session
            
        Returns:
            Session: New session object
        """
        # Create a completion to start the session
        response = self.chat.create(params)
        
        # Extract session ID from response
        session_id = response.get("session_id")
        if not session_id:
            raise ValueError("Failed to create session: No session ID returned")
        
        # Return a session object
        return Session(self.client, session_id)
    
    def resume(self, session_id: str) -> Session:
        """
        Resume an existing session
        
        Args:
            session_id: ID of the session to resume
            
        Returns:
            Session: Resumed session object
        """
        return Session(self.client, session_id)