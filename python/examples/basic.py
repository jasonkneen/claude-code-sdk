"""
Basic usage example for Claude Code SDK
"""

import os
from claude_code_sdk import ClaudeCode

# Initialize the client
claude = ClaudeCode(options={
    "api_key": os.environ.get("ANTHROPIC_API_KEY")
})

# Use OpenAI-style completions API
def generate_code():
    response = claude.chat["completions"].create({
        "model": "claude-code",
        "messages": [
            {"role": "user", "content": "Write a Python function to read CSV files"}
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
    })
    
    print(response["choices"][0]["message"]["content"])

# Use Anthropic-style messages API
def generate_code_anthropic():
    response = claude.messages.create({
        "model": "claude-code",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Write a Python function to read CSV files"}
                ]
            }
        ],
        "max_tokens": 1000,
    })
    
    print(response["content"][0]["text"])

# Session management example
def code_session():
    # Start a session
    session = claude.sessions.create({
        "messages": [
            {"role": "user", "content": "Let's create a Python project"}
        ]
    })
    
    # Continue the session
    response = session.continue_session({
        "messages": [
            {"role": "user", "content": "Now add a database connection"}
        ]
    })
    
    print(response["choices"][0]["message"]["content"])

# Tool usage example
def use_tools():
    # Register a tool
    claude.tools.create({
        "name": "filesystem",
        "description": "Access the filesystem",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    })
    
    # Use the tool in a chat completion
    response = claude.chat["completions"].create({
        "model": "claude-code",
        "messages": [
            {"role": "user", "content": "Read my README.md file"}
        ],
        "tools": [{"name": "filesystem"}]
    })
    
    print(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    generate_code()