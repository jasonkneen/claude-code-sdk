"""
Tools API for Claude Code SDK
"""

from typing import Dict, List, Any, Optional

from claude_code_sdk.client.base import BaseClient


class Tools:
    """Tools API for Claude Code"""
    
    def __init__(self, client: BaseClient):
        """
        Initialize tools API
        
        Args:
            client: Base client instance
        """
        self.client = client
        self._registered_tools = {}
        
    def create(self, tool_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new tool
        
        Args:
            tool_definition: Tool definition
            
        Returns:
            Dict: Registered tool
        """
        # Store the tool definition
        name = tool_definition.get("name")
        if not name:
            raise ValueError("Tool definition must include a name")
            
        self._registered_tools[name] = tool_definition
        return tool_definition
    
    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a registered tool by name
        
        Args:
            name: Tool name
            
        Returns:
            Optional[Dict]: Tool definition or None if not found
        """
        return self._registered_tools.get(name)
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List all registered tools
        
        Returns:
            List[Dict]: List of tool definitions
        """
        return list(self._registered_tools.values())
    
    def delete(self, name: str) -> bool:
        """
        Delete a registered tool
        
        Args:
            name: Tool name
            
        Returns:
            bool: True if deleted, False if not found
        """
        if name in self._registered_tools:
            del self._registered_tools[name]
            return True
        return False