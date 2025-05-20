# Claude Code SDK - Python

A Python wrapper for Claude Code CLI that provides a seamless, type-safe API compatible with both OpenAI and Anthropic SDKs.

## Installation

First, install the Claude Code CLI:

```bash
npm install -g @anthropic-ai/claude-code
```

Then install the wrapper:

```bash
pip install claude-code-sdk
```

For development installation:

```bash
git clone https://github.com/anthropics/claude-code-sdk.git
cd claude-code-sdk/python
pip install -e .
```

## Setup

You'll need an Anthropic API key to use Claude Code. You can either set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Or provide it when initializing the client:

```python
from claude_code_sdk import ClaudeCode

claude = ClaudeCode(options={
    "api_key": "your_api_key_here"
})
```

## Usage

This SDK provides both OpenAI-style and Anthropic-style APIs for interacting with Claude Code.

### OpenAI Style API

```python
from claude_code_sdk import ClaudeCode

# Create a client
claude = ClaudeCode()

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

# Streaming example
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
```

### Anthropic Style API

```python
from claude_code_sdk import ClaudeCode

# Create a client
claude = ClaudeCode()

# Use Anthropic-style messages API
def generate_code():
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

# Streaming example
async def stream_code():
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
```

### Session Management

```python
from claude_code_sdk import ClaudeCode

claude = ClaudeCode()

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
```

### Tools

```python
from claude_code_sdk import ClaudeCode

claude = ClaudeCode()

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
```

## Debugging

To test if the Claude Code CLI is installed and configured correctly, run:

```bash
npx claude -h
```

If you experience issues, set more verbose output:

```python
claude = ClaudeCode(options={
    "api_key": os.environ.get("ANTHROPIC_API_KEY"),
    "cli_path": "/path/to/claude",  # If claude isn't in your PATH
    "timeout": 60000  # Longer timeout (ms)
})
```

## Features

- OpenAI-compatible `chat["completions"].create()` method
- Anthropic-compatible `messages.create()` method
- Session management for multi-turn conversations
- Tool registration and usage
- Full type hints
- Streaming responses
- Batch operations

## Requirements

- Python 3.7+
- @anthropic-ai/claude-code CLI installed

## Development

### Publishing to PyPI

To publish a new version to PyPI, use the provided script:

```bash
cd python
./scripts/publish.sh
```

For detailed instructions, see [PUBLISHING.md](PUBLISHING.md).

## License

MIT