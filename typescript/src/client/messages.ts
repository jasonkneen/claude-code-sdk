import { Readable } from 'stream'
import { BaseClient } from './base'
import {
  AnthropicMessageResponse,
  AnthropicMessageCreateParams,
  AnthropicMessageStreamPart,
} from '../types'
import {
  convertMessagesToPrompt,
  parseCliOutput,
} from '../implementations/converters'

// Class for Anthropic-style messages
export class Messages {
  private client: BaseClient

  constructor(client: BaseClient) {
    this.client = client
  }

  /**
   * Create a message (Anthropic style)
   */
  async create(params: AnthropicMessageCreateParams): Promise<AnthropicMessageResponse> {
    // Convert the Anthropic-style parameters to CLI parameters
    const prompt = convertMessagesToPrompt(params.messages)
    
    const cliParams = {
      prompt,
      outputFormat: 'json' as const,
      temperature: params.temperature,
      maxTokens: params.max_tokens,
      topP: params.top_p,
      stop: params.stop_sequences ? params.stop_sequences.join(',') : undefined,
      timeout: params.timeout,
    }
    
    // Handle tools if provided
    if (params.tools && params.tools.length > 0) {
      const toolNames = params.tools.map((tool) => tool.name)
      // Use index signature to add allowedTools property
      ;(cliParams as { allowedTools?: string[] }).allowedTools = toolNames
    }

    if (params.stream) {
      // Create streaming response
      return this.createStream(params) as unknown as AnthropicMessageResponse
    } else {
      // Execute and parse response
      const output = await this.client['executeCommand'](cliParams)
      return parseCliOutput<AnthropicMessageResponse>(output)
    }
  }

  /**
   * Create a streaming message (Anthropic style)
   */
  createStream(params: AnthropicMessageCreateParams): AsyncIterable<AnthropicMessageStreamPart> {
    // Convert the Anthropic-style parameters to CLI parameters
    const prompt = convertMessagesToPrompt(params.messages)
    
    const cliParams = {
      prompt,
      outputFormat: 'stream-json' as const,
      temperature: params.temperature,
      maxTokens: params.max_tokens,
      topP: params.top_p,
      stop: params.stop_sequences ? params.stop_sequences.join(',') : undefined,
      timeout: params.timeout,
    }
    
    // Handle tools if provided
    if (params.tools && params.tools.length > 0) {
      const toolNames = params.tools.map((tool) => tool.name)
      // Use index signature to add allowedTools property
      ;(cliParams as { allowedTools?: string[] }).allowedTools = toolNames
    }

    // Get streaming response
    const stream = this.client['executeStreamCommand'](cliParams) as Readable

    // Create an async iterator from the stream
    const asyncIterator: AsyncIterable<AnthropicMessageStreamPart> = {
      [Symbol.asyncIterator]() {
        return {
          next(): Promise<IteratorResult<AnthropicMessageStreamPart>> {
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
                      const chunk = JSON.parse(jsonStr) as AnthropicMessageStreamPart
                      resolve({ done: false, value: chunk })
                      return
                    } catch (e) {
                      // Skip invalid JSON
                      console.warn('Invalid JSON in stream chunk:', jsonStr)
                    }
                  }
                  
                  // If we couldn't parse anything, resolve with empty chunk
                  resolve({ done: false, value: {} as AnthropicMessageStreamPart })
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
   * Batch create messages (custom extension)
   */
  async batchCreate(params: AnthropicMessageCreateParams[]): Promise<AnthropicMessageResponse[]> {
    return Promise.all(params.map(p => this.create(p)))
  }
}