# Claude Code SDK

A TypeScript wrapper for Claude Code CLI that provides a seamless, type-safe API compatible with both OpenAI and Anthropic SDKs.

## Installation

First, install the Claude Code CLI:

```bash
npm install -g @anthropic-ai/claude-code
```

Then install the wrapper using one of these methods:

```bash
# Using npm
npm install claude-code-sdk

# Using yarn
yarn add claude-code-sdk

# Using pnpm
pnpm add claude-code-sdk
```

## Setup

You'll need an Anthropic API key to use Claude Code. You can either set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Or provide it when initializing the client:

```typescript
import { ClaudeCode } from 'claude-code-sdk'

const claude = new ClaudeCode({
  apiKey: 'your_api_key_here'
})
```

## Usage

This SDK provides both OpenAI-style and Anthropic-style APIs for interacting with Claude Code.

### OpenAI Style API

```typescript
import { ClaudeCode } from 'claude-code-sdk'

// Create a client
const claude = new ClaudeCode()

// Use OpenAI-style completions API
async function generateCode() {
  const response = await claude.chat.completions.create({
    model: 'claude-code',
    messages: [
      { role: 'user', content: 'Write a TypeScript function to read CSV files' }
    ],
    max_tokens: 1000,
    temperature: 0.7,
  })

  console.log(response.choices[0].message.content)
}

// Streaming example
async function streamCode() {
  const stream = await claude.chat.completions.createStream({
    model: 'claude-code',
    messages: [
      { role: 'user', content: 'Create a React component for a login form' }
    ]
  })

  for await (const chunk of stream) {
    if (chunk.choices[0].delta.content) {
      process.stdout.write(chunk.choices[0].delta.content)
    }
  }
}
```

### Anthropic Style API

```typescript
import { ClaudeCode } from 'claude-code-sdk'

// Create a client
const claude = new ClaudeCode()

// Use Anthropic-style messages API
async function generateCode() {
  const response = await claude.messages.create({
    model: 'claude-code',
    messages: [
      { 
        role: 'user', 
        content: [{ 
          type: 'text', 
          text: 'Write a TypeScript function to read CSV files' 
        }] 
      }
    ],
    max_tokens: 1000,
  })

  console.log(response.content[0].text)
}

// Streaming example
async function streamCode() {
  const stream = await claude.messages.createStream({
    model: 'claude-code',
    messages: [
      { 
        role: 'user', 
        content: [{ 
          type: 'text', 
          text: 'Create a React component for a login form' 
        }] 
      }
    ]
  })

  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta' && chunk.delta?.text) {
      process.stdout.write(chunk.delta.text)
    }
  }
}
```

### Session Management

```typescript
import { ClaudeCode } from 'claude-code-sdk'

const claude = new ClaudeCode()

async function codeSession() {
  // Start a session
  const session = await claude.sessions.create({
    messages: [
      { role: 'user', content: 'Let\'s create a TypeScript project' }
    ]
  })

  // Continue the session
  const response = await session.continue({
    messages: [
      { role: 'user', content: 'Now add a database connection' }
    ]
  })

  console.log(response.choices[0].message.content)
}
```

### Tools

```typescript
import { ClaudeCode } from 'claude-code-sdk'

const claude = new ClaudeCode()

async function useTools() {
  // Register a tool
  await claude.tools.create({
    name: 'filesystem',
    description: 'Access the filesystem',
    input_schema: {
      type: 'object',
      properties: {
        path: { type: 'string' }
      },
      required: ['path']
    }
  })

  // Use the tool in a chat completion
  const response = await claude.chat.completions.create({
    model: 'claude-code',
    messages: [
      { role: 'user', content: 'Read my README.md file' }
    ],
    tools: [{ name: 'filesystem' }]
  })

  console.log(response.choices[0].message.content)
}
```

## Debugging

To test if the Claude Code CLI is installed and configured correctly, run:

```bash
npx claude -h
```

If you experience issues, set more verbose output:

```typescript
const claude = new ClaudeCode({
  apiKey: process.env.ANTHROPIC_API_KEY,
  cliPath: '/path/to/claude', // If claude isn't in your PATH
  timeout: 60000 // Longer timeout (ms)
})
```

## Features

- OpenAI-compatible `chat.completions.create` method
- Anthropic-compatible `messages.create` method
- Session management for multi-turn conversations
- Tool registration and usage
- Full TypeScript support
- Streaming responses
- Batch operations

## Requirements

- Node.js v16+
- TypeScript 4.5+
- @anthropic-ai/claude-code CLI installed

## License

MIT