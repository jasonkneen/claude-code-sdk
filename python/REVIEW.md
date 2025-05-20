# Claude Code SDK Python Implementation

## Overview
This is a Python implementation of the Claude Code SDK, providing a wrapper around the Claude Code CLI. The implementation follows the same patterns as the TypeScript version, offering both OpenAI-compatible and Anthropic-compatible APIs.

## Key Features
- **OpenAI-compatible API**: Use `chat["completions"].create()` with familiar parameters
- **Anthropic-compatible API**: Use `messages.create()` with Anthropic's message format
- **Session Management**: Create and resume conversations with `sessions.create()`
- **Tool Support**: Register and use tools with `tools.create()`
- **Streaming Support**: Stream responses with `create_stream()` methods
- **Error Handling**: Consistent error handling with status codes

## Implementation Details
The Python SDK is structured similarly to the TypeScript version:

- **Client Classes**: Base client, chat completions, messages, sessions, and tools
- **CLI Executor**: Handles subprocess management and command execution
- **Converters**: Transform between different API formats
- **Type Definitions**: Provide type hints for better IDE support

## Alignment with Official SDK
This implementation aligns with Anthropic's official SDK documentation, supporting:
- Basic SDK usage patterns
- Advanced features like multi-turn conversations
- Custom system prompts
- MCP configuration
- Multiple output formats (text, JSON, stream-JSON)
- Proper message schema handling

## Usage Examples
The SDK includes example scripts demonstrating:
- Basic usage with OpenAI and Anthropic APIs
- Streaming responses
- Session management
- Tool registration and usage

## Development Status
This is a Python implementation of the Claude Code SDK based on the TypeScript version. Anthropic has mentioned that official Python SDKs are coming soon, which may replace or complement this implementation.