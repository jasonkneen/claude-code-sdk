// Common types used across both OpenAI and Anthropic style APIs

export type Role = 'user' | 'assistant' | 'system'

// OpenAI Style Types
export interface OpenAIMessage {
  role: Role
  content: string
  files?: Array<FileReference>
}

export interface OpenAIFunction {
  name: string
  description?: string
  parameters?: Record<string, unknown>
}

export interface OpenAITool {
  type: 'function'
  function: OpenAIFunction
}

export interface OpenAICompletionChoice {
  index: number
  message: {
    role: Role
    content: string
  }
  finish_reason: string
}

export interface OpenAIStreamChoice {
  index: number
  delta: {
    role?: Role
    content?: string
  }
  finish_reason: string | null
}

export interface OpenAIUsage {
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
}

export interface OpenAIChatCompletion {
  id: string
  object: 'chat.completion'
  created: number
  model: string
  choices: Array<OpenAICompletionChoice>
  usage: OpenAIUsage
}

export interface OpenAIChatCompletionChunk {
  id: string
  object: 'chat.completion.chunk'
  created: number
  model: string
  choices: Array<OpenAIStreamChoice>
}

export interface OpenAIChatCompletionCreateParams {
  model: string
  messages: Array<OpenAIMessage>
  temperature?: number
  max_tokens?: number
  top_p?: number
  tools?: Array<OpenAITool>
  stream?: boolean
  stop?: string | Array<string>
  timeout?: number
}

// Anthropic Style Types
export interface ContentBlock {
  type: 'text' | 'image'
  text?: string
  source?: {
    type: 'base64' | 'url'
    media_type: string
    data: string
  }
}

export interface AnthropicMessage {
  role: Role
  content: string | Array<ContentBlock>
  files?: Array<FileReference>
}

export interface AnthropicTool {
  name: string
  description?: string
  input_schema: Record<string, unknown>
}

export interface AnthropicUsage {
  input_tokens: number
  output_tokens: number
}

export interface AnthropicMessageResponse {
  id: string
  type: 'message'
  role: 'assistant'
  model: string
  content: Array<ContentBlock>
  usage: AnthropicUsage
  stop_reason: string
}

export interface AnthropicMessageStreamPart {
  type: 'content_block_start' | 'content_block_delta' | 'content_block_stop' | 'message_stop'
  index?: number
  delta?: {
    type?: string
    text?: string
  }
}

export interface AnthropicMessageCreateParams {
  model: string
  messages: Array<AnthropicMessage>
  max_tokens?: number
  temperature?: number
  top_p?: number
  tools?: Array<AnthropicTool>
  stream?: boolean
  stop_sequences?: Array<string>
  timeout?: number
}

// Common File Reference Type
export interface FileReference {
  path: string
  content?: string
}

// Claude Code Specific Types
export interface ClaudeCodeError extends Error {
  status?: number
  code?: string
  param?: string
}

export interface SessionParams {
  messages: Array<OpenAIMessage | AnthropicMessage>
  model?: string
}

export interface SessionContinueParams {
  messages: Array<OpenAIMessage | AnthropicMessage>
}

// Common Options Type
export interface ClaudeCodeOptions {
  apiKey?: string
  cliPath?: string
  timeout?: number
}

// Automation Types
export interface AutomationOptions {
  type: 'github-review' | 'github-pr' | 'jira-ticket'
  config?: Record<string, unknown>
}