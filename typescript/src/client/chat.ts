import { Readable } from 'stream'
import { BaseClient } from './base'
import {
  OpenAIChatCompletion,
  OpenAIChatCompletionCreateParams,
  OpenAIChatCompletionChunk,
} from '../types'
import {
  convertMessagesToPrompt,
  parseCliOutput,
  convertOpenAIToAnthropicTools,
} from '../implementations/converters'

// Class for OpenAI-style completions
export class ChatCompletions {
  private client: BaseClient

  constructor(client: BaseClient) {
    this.client = client
  }

  /**
   * Create a completion (OpenAI style)
   */
  async create(params: OpenAIChatCompletionCreateParams): Promise<OpenAIChatCompletion> {
    // Convert the OpenAI-style parameters to CLI parameters
    const prompt = convertMessagesToPrompt(params.messages)
    
    const cliParams = {
      prompt,
      outputFormat: 'json' as const,
      temperature: params.temperature,
      maxTokens: params.max_tokens,
      topP: params.top_p,
      stop: params.stop ? 
        (Array.isArray(params.stop) ? params.stop.join(',') : params.stop) : 
        undefined,
      timeout: params.timeout,
    }
    
    // Handle tools if provided
    if (params.tools && params.tools.length > 0) {
      const anthropicTools = convertOpenAIToAnthropicTools(params.tools)
      const toolNames = anthropicTools.map((tool) => tool.name)
      // Use index signature to add allowedTools property
      ;(cliParams as { allowedTools?: string[] }).allowedTools = toolNames
    }

    if (params.stream) {
      // Create streaming response
      return this.createStream(params) as unknown as OpenAIChatCompletion
    } else {
      // Execute and parse response
      const output = await this.client['executeCommand'](cliParams)
      return parseCliOutput<OpenAIChatCompletion>(output)
    }
  }

  /**
   * Create a streaming completion (OpenAI style)
   */
  createStream(params: OpenAIChatCompletionCreateParams): AsyncIterable<OpenAIChatCompletionChunk> {
    // Convert the OpenAI-style parameters to CLI parameters
    const prompt = convertMessagesToPrompt(params.messages)
    
    const cliParams = {
      prompt,
      outputFormat: 'stream-json' as const,
      temperature: params.temperature,
      maxTokens: params.max_tokens,
      topP: params.top_p,
      stop: params.stop ? 
        (Array.isArray(params.stop) ? params.stop.join(',') : params.stop) : 
        undefined,
      timeout: params.timeout,
    }
    
    // Handle tools if provided
    if (params.tools && params.tools.length > 0) {
      const anthropicTools = convertOpenAIToAnthropicTools(params.tools)
      const toolNames = anthropicTools.map((tool) => tool.name)
      // Use index signature to add allowedTools property
      ;(cliParams as { allowedTools?: string[] }).allowedTools = toolNames
    }

    // Get streaming response
    const stream = this.client['executeStreamCommand'](cliParams) as Readable

    // Create an async iterator from the stream
    const asyncIterator: AsyncIterable<OpenAIChatCompletionChunk> = {
      [Symbol.asyncIterator]() {
        return {
          next(): Promise<IteratorResult<OpenAIChatCompletionChunk>> {
            return new Promise((resolve, reject) => {
              stream.once('data', (data: Buffer) => {
                try {
                  // Parse each chunk as a separate JSON object
                  const chunkStr = data.toString().trim()
                  
                  // Handle potential multiple JSON objects in one chunk
                  const jsonStrings = chunkStr
                    .split('\n')
                    .filter(s => s.trim().length > 0)
                    
                  for (const jsonStr of jsonStrings) {
                    try {
                      const chunk = JSON.parse(jsonStr) as OpenAIChatCompletionChunk
                      resolve({ done: false, value: chunk })
                      return
                    } catch (e) {
                      // Skip invalid JSON
                      console.warn('Invalid JSON in stream chunk:', jsonStr)
                    }
                  }
                  
                  // If we couldn't parse anything, resolve with empty chunk
                  resolve({ done: false, value: {} as OpenAIChatCompletionChunk })
                } catch (error) {
                  reject(error)
                }
              })

              stream.once('end', () => {
                resolve({ done: true, value: undefined })
              })

              stream.once('error', (error) => {
                reject(error)
              })
            })
          }
        }
      }
    }

    return asyncIterator
  }

  /**
   * Batch create completions (custom extension)
   */
  async batchCreate(params: OpenAIChatCompletionCreateParams[]): Promise<OpenAIChatCompletion[]> {
    return Promise.all(params.map(p => this.create(p)))
  }
}