# Claude Code SDK

A wrapper for Claude Code CLI that provides a seamless, type-safe API compatible with both OpenAI and Anthropic SDKs. This monorepo contains both TypeScript and Python implementations.

## Overview

This SDK lets developers interact with Claude Code using familiar OpenAI or Anthropic-style APIs. The SDK wraps the Claude Code CLI, providing both:

- **TypeScript Implementation**: For Node.js and TypeScript projects
- **Python Implementation**: For Python applications and scripts

## Features

- OpenAI-compatible API methods
- Anthropic-compatible API methods
- Session management for multi-turn conversations
- Tool registration and usage
- Full type support
- Streaming responses
- Batch operations

## Implementations

- [TypeScript SDK](typescript/README.md)
- [Python SDK](python/README.md)

## Installation

Each implementation has its own installation instructions:

- For TypeScript: See [TypeScript Installation](typescript/README.md#installation)
- For Python: See [Python Installation](python/README.md#installation)

Both implementations require the Claude Code CLI to be installed:

```bash
npm install -g @anthropic-ai/claude-code
```

## Requirements

- Node.js v16+ (for TypeScript)
- Python 3.7+ (for Python)
- @anthropic-ai/claude-code CLI installed

## Contributing

Please see the [Contributing Guide](CONTRIBUTING.md) for details on how to contribute to the project.

## License

[MIT](LICENSE)