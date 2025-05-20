import { BaseClient } from './base'
import { ChatCompletions } from './chat'
import { Messages } from './messages'
import { Sessions } from './sessions'
import { Tools } from './tools'
import { ClaudeCodeOptions } from '../types'

// Main client class
export class ClaudeCode extends BaseClient {
  readonly chat: { completions: ChatCompletions }
  readonly messages: Messages
  readonly sessions: Sessions
  readonly tools: Tools

  constructor(options: ClaudeCodeOptions = {}) {
    super(options)

    // Initialize OpenAI-style chat completions
    const completionsInstance = new ChatCompletions(this)
    this.chat = {
      completions: completionsInstance,
    }

    // Initialize Anthropic-style messages
    this.messages = new Messages(this)

    // Initialize sessions
    this.sessions = new Sessions(this)

    // Initialize tools
    this.tools = new Tools(this)
  }

  // Convenience method for configuring MCP server URL
  setMcpServer(url: string): void {
    process.env.CLAUDE_CODE_MCP_URL = url
  }
}