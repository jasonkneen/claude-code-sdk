import { ClaudeCliExecutor, ClaudeExecParams } from '../implementations/cli'
import { ClaudeCodeOptions, ClaudeCodeError } from '../types'

export class BaseClient {
  protected executor: ClaudeCliExecutor
  protected apiKey?: string
  protected defaultModel: string = 'claude-code'
  protected defaultTimeout: number

  constructor(options: ClaudeCodeOptions = {}) {
    this.apiKey = options.apiKey || process.env.ANTHROPIC_API_KEY
    this.defaultTimeout = options.timeout || 300000 // 5 minutes default

    this.executor = new ClaudeCliExecutor({
      cliPath: options.cliPath || '@anthropic-ai/claude-code',
      timeout: this.defaultTimeout,
      env: {
        ...(this.apiKey ? { ANTHROPIC_API_KEY: this.apiKey } : {}),
      },
    })
  }

  /**
   * Creates an error object in the style of OpenAI/Anthropic SDKs
   */
  protected createError(message: string, status: number = 500, code?: string): ClaudeCodeError {
    const error = new Error(message) as ClaudeCodeError
    error.status = status
    error.code = code
    return error
  }

  /**
   * Executes a Claude CLI command with error handling
   */
  protected async executeCommand(params: ClaudeExecParams): Promise<string> {
    try {
      return await this.executor.execute(params)
    } catch (error) {
      const err = error as Error
      throw this.createError(err.message, (err as unknown as { status?: number }).status)
    }
  }

  /**
   * Creates a streaming response from Claude CLI
   */
  protected executeStreamCommand(params: ClaudeExecParams): NodeJS.ReadableStream {
    return this.executor.executeStream(params)
  }
}