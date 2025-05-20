import { exec } from 'child_process'
import { promisify } from 'util'
import { Readable } from 'stream'

const execP = promisify(exec)

export interface ClaudeExecOptions {
  cliPath?: string
  timeout?: number
  env?: NodeJS.ProcessEnv
}

export type OutputFormat = 'text' | 'json' | 'stream-json'

export interface ClaudeExecParams {
  prompt?: string
  outputFormat?: OutputFormat
  systemPrompt?: string
  continue?: boolean
  resume?: string
  allowedTools?: string[]
  disallowedTools?: string[]
  mcpConfig?: string
  maxTurns?: number
  maxTokens?: number
  temperature?: number
  topP?: number
  stop?: string
  timeout?: number
  [key: string]: unknown
}

export class ClaudeCliExecutor {
  private cliPath: string
  private defaultTimeout: number
  private env: NodeJS.ProcessEnv

  constructor(options: ClaudeExecOptions = {}) {
    this.cliPath = options.cliPath || '@anthropic-ai/claude-code'
    this.defaultTimeout = options.timeout || 300000 // 5 minutes default
    this.env = { ...process.env, ...(options.env || {}) }
  }

  /**
   * Builds arguments array for the Claude CLI based on provided parameters
   */
  private buildArgs(params: ClaudeExecParams): string[] {
    const args: string[] = []

    if (params.prompt) {
      args.push('-p')
      args.push(params.prompt)
    }

    if (params.outputFormat) {
      args.push('--output-format')
      args.push(params.outputFormat)
    }

    if (params.systemPrompt) {
      args.push('--system-prompt')
      args.push(params.systemPrompt)
    }

    if (params.continue) {
      args.push('--continue')
    }

    if (params.resume) {
      args.push('--resume')
      args.push(params.resume)
    }

    if (params.allowedTools && params.allowedTools.length > 0) {
      args.push('--allowedTools')
      args.push(params.allowedTools.join(','))
    }

    if (params.disallowedTools && params.disallowedTools.length > 0) {
      args.push('--disallowedTools')
      args.push(params.disallowedTools.join(','))
    }

    if (params.mcpConfig) {
      args.push('--mcp-config')
      args.push(params.mcpConfig)
    }

    if (params.maxTurns) {
      args.push('--max-turns')
      args.push(String(params.maxTurns))
    }

    // Add any additional parameters provided
    for (const [key, value] of Object.entries(params)) {
      if (
        !['prompt', 'outputFormat', 'systemPrompt', 'continue', 'resume', 'allowedTools', 
          'disallowedTools', 'mcpConfig', 'maxTurns'].includes(key) && 
        value !== undefined
      ) {
        // Convert camelCase to kebab-case for CLI flags
        const kebabKey = key.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()
        args.push(`--${kebabKey}`)
        args.push(String(value))
      }
    }

    return args
  }

  /**
   * Execute a Claude CLI command and return the result
   */
  public async execute(params: ClaudeExecParams, timeout?: number): Promise<string> {
    const args = this.buildArgs(params)
    const timeoutMs = timeout || this.defaultTimeout

    return new Promise<string>((resolve, reject) => {
      // Use spawn for better handling of arguments
      const { spawn } = require('child_process')
      const childProcess = spawn(this.cliPath, args, { 
        env: this.env,
      })
      
      let stdout = ''
      let stderr = ''
      
      // Set timeout
      const timeoutId = setTimeout(() => {
        childProcess.kill()
        const error = new Error(`Claude CLI execution timed out after ${timeoutMs}ms`) as Error & { status?: number; code?: string }
        error.status = 408
        reject(error)
      }, timeoutMs)
      
      childProcess.stdout.on('data', (data: Buffer) => {
        stdout += String(data)
      })
      
      childProcess.stderr.on('data', (data: Buffer) => {
        stderr += String(data)
      })
      
      childProcess.on('error', (error: Error) => {
        clearTimeout(timeoutId)
        
        // Create a more informative error
        const enhancedError = new Error(
          `Claude CLI execution failed: ${error.message}${stderr ? `\nStderr: ${stderr}` : ''}`
        ) as Error & { status?: number; code?: string }
        
        // Add status code for OpenAI/Anthropic compatibility
        enhancedError.status = 500
        
        reject(enhancedError)
      })
      
      childProcess.on('close', (code: number) => {
        clearTimeout(timeoutId)
        
        if (code !== 0) {
          // Create a more informative error
          const enhancedError = new Error(
            `Claude CLI process exited with code ${code}${stderr ? `\nStderr: ${stderr}` : ''}`
          ) as Error & { status?: number; code?: string }
          
          // Add status code for OpenAI/Anthropic compatibility
          enhancedError.status = code || 500
          
          reject(enhancedError)
        } else {
          if (stderr) {
            console.error('Claude CLI stderr:', stderr)
          }
          
          resolve(stdout)
        }
      })
    })
  }

  /**
   * Execute a Claude CLI command in streaming mode and return a readable stream
   */
  public executeStream(params: ClaudeExecParams): Readable {
    // Ensure we use stream-json format for streaming
    const streamParams = { ...params, outputFormat: 'stream-json' as const }
    
    // Build the arguments array
    const args = this.buildArgs(streamParams)

    // Create a child process for streaming
    const { spawn } = require('child_process')
    const childProcess = spawn(this.cliPath, args, { env: this.env })
    
    // Create a readable stream to return to the caller
    const outputStream = new Readable({
      read() {} // Implementation required but not used
    })

    // Handle data events
    childProcess.stdout.on('data', (data: Buffer) => {
      outputStream.push(data)
    })

    // Handle errors and close events
    childProcess.stderr.on('data', (data: Buffer) => {
      console.error('Claude CLI Stream stderr:', String(data))
    })

    childProcess.on('error', (error: Error) => {
      outputStream.emit('error', error)
      outputStream.push(null) // End the stream
    })

    childProcess.on('close', (code: number) => {
      if (code !== 0) {
        outputStream.emit('error', new Error(`Claude CLI process exited with code ${code}`))
      }
      outputStream.push(null) // End the stream
    })

    return outputStream
  }
}