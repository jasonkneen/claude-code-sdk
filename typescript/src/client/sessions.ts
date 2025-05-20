import { BaseClient } from './base'
import {
  OpenAIMessage,
  AnthropicMessage,
  OpenAIChatCompletion,
  AnthropicMessageResponse,
  SessionParams,
  SessionContinueParams,
} from '../types'
import {
  convertMessagesToPrompt,
  parseCliOutput,
} from '../implementations/converters'

// Class for session management
export class Sessions {
  private client: BaseClient

  constructor(client: BaseClient) {
    this.client = client
  }

  /**
   * Create a new session
   */
  async create(params: SessionParams): Promise<Session> {
    // Convert messages to prompt
    const prompt = convertMessagesToPrompt(params.messages)
    
    // Start a new session
    const cliParams = {
      prompt,
      outputFormat: 'json' as const,
    }

    // Execute command and get initial response
    const output = await this.client['executeCommand'](cliParams)
    const response = parseCliOutput<Record<string, unknown>>(output)
    
    // Extract session ID if present
    const sessionId = (response as { id?: string }).id || 
                      `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
    
    // Create and return a new session
    return new Session(sessionId, this.client, params.messages)
  }

  /**
   * Resume an existing session by ID
   */
  async resume(sessionId: string): Promise<Session> {
    // Resume a session by ID
    const cliParams = {
      resume: sessionId,
      outputFormat: 'json' as const,
    }

    // Execute command to resume session
    await this.client['executeCommand'](cliParams)
    
    // Create and return session object
    return new Session(sessionId, this.client, [])
  }
}

// Individual session class
export class Session {
  readonly id: string
  private client: BaseClient
  private messages: Array<OpenAIMessage | AnthropicMessage>

  constructor(id: string, client: BaseClient, messages: Array<OpenAIMessage | AnthropicMessage>) {
    this.id = id
    this.client = client
    this.messages = [...messages]
  }

  /**
   * Continue a session with additional messages
   */
  async continue(params: SessionContinueParams): Promise<OpenAIChatCompletion | AnthropicMessageResponse> {
    // Add new messages to the existing ones
    this.messages = [...this.messages, ...params.messages]
    
    // Convert messages to prompt
    const prompt = convertMessagesToPrompt(params.messages)
    
    // Continue the session
    const cliParams = {
      prompt,
      resume: this.id,
      outputFormat: 'json' as const,
    }

    // Execute command and get response
    const output = await this.client['executeCommand'](cliParams)
    return parseCliOutput<OpenAIChatCompletion>(output)
  }

  /**
   * Get all messages in this session
   */
  getMessages(): Array<OpenAIMessage | AnthropicMessage> {
    return [...this.messages]
  }
}