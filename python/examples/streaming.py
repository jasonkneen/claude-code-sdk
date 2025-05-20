"""
Streaming example for Claude Code SDK
"""

import os
import asyncio
from claude_code_sdk import ClaudeCode

# Initialize the client
claude = ClaudeCode(options={
    "api_key": os.environ.get("ANTHROPIC_API_KEY")
})

# OpenAI-style streaming
async def stream_code():
    stream = claude.chat["completions"].create_stream({
        "model": "claude-code",
        "messages": [
            {"role": "user", "content": "Create a Python class for a login form"}
        ],
        "stream": True
    })
    
    async for chunk in stream:
        if "choices" in chunk and chunk["choices"] and "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                print(delta["content"], end="", flush=True)

# Anthropic-style streaming
async def stream_code_anthropic():
    stream = claude.messages.create_stream({
        "model": "claude-code",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Create a Python class for a login form"}
                ]
            }
        ],
        "stream": True
    })
    
    async for chunk in stream:
        if chunk.get("type") == "content_block_delta" and "delta" in chunk:
            delta = chunk["delta"]
            if "text" in delta:
                print(delta["text"], end="", flush=True)

# Session streaming
async def stream_session():
    # Start a session
    session = claude.sessions.create({
        "messages": [
            {"role": "user", "content": "Let's create a Python project"}
        ]
    })
    
    # Continue the session with streaming
    stream = session.continue_stream({
        "messages": [
            {"role": "user", "content": "Now add a database connection"}
        ]
    })
    
    async for chunk in stream:
        if "choices" in chunk and chunk["choices"] and "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                print(delta["content"], end="", flush=True)

if __name__ == "__main__":
    asyncio.run(stream_code())