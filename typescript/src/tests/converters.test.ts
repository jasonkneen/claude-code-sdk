import { describe, it, expect } from 'vitest'
import {
  convertOpenAIToAnthropicMessage,
  convertAnthropicToOpenAIMessage,
  convertOpenAIToAnthropicTools,
  convertAnthropicToOpenAITools,
  convertMessagesToPrompt,
  parseCliOutput
} from '../implementations/converters'
import { AnthropicMessage, OpenAIMessage, OpenAITool, AnthropicTool } from '../types'

describe('Converter utilities', () => {
  describe('convertOpenAIToAnthropicMessage', () => {
    it('should convert OpenAI message to Anthropic format', () => {
      const openAIMessage: OpenAIMessage = {
        role: 'user',
        content: 'Test message'
      }

      const anthropicMessage = convertOpenAIToAnthropicMessage(openAIMessage)
      
      expect(anthropicMessage.role).toBe('user')
      expect(Array.isArray(anthropicMessage.content)).toBe(true)
      expect((anthropicMessage.content as any)[0].type).toBe('text')
      expect((anthropicMessage.content as any)[0].text).toBe('Test message')
    })

    it('should preserve file references when converting', () => {
      const openAIMessage: OpenAIMessage = {
        role: 'user',
        content: 'Analyze this file',
        files: [{ path: 'test.ts', content: 'const a = 1;' }]
      }

      const anthropicMessage = convertOpenAIToAnthropicMessage(openAIMessage)
      
      expect(anthropicMessage.files).toBeDefined()
      expect(anthropicMessage.files?.[0].path).toBe('test.ts')
      expect(anthropicMessage.files?.[0].content).toBe('const a = 1;')
    })
  })

  describe('convertAnthropicToOpenAIMessage', () => {
    it('should convert Anthropic message to OpenAI format', () => {
      const anthropicMessage: AnthropicMessage = {
        role: 'user',
        content: [
          { type: 'text', text: 'Text part 1' },
          { type: 'text', text: 'Text part 2' }
        ]
      }

      const openAIMessage = convertAnthropicToOpenAIMessage(anthropicMessage)
      
      expect(openAIMessage.role).toBe('user')
      expect(typeof openAIMessage.content).toBe('string')
      expect(openAIMessage.content).toBe('Text part 1\nText part 2')
    })

    it('should handle string content in Anthropic format', () => {
      const anthropicMessage = {
        role: 'user',
        content: 'Already string content'
      } as AnthropicMessage

      const openAIMessage = convertAnthropicToOpenAIMessage(anthropicMessage)
      
      expect(openAIMessage.role).toBe('user')
      expect(openAIMessage.content).toBe('Already string content')
    })
  })

  describe('convertOpenAIToAnthropicTools', () => {
    it('should convert OpenAI tools to Anthropic format', () => {
      const openAITools: OpenAITool[] = [
        {
          type: 'function',
          function: {
            name: 'get_weather',
            description: 'Get the weather for a location',
            parameters: {
              type: 'object',
              properties: {
                location: { type: 'string' }
              }
            }
          }
        }
      ]

      const anthropicTools = convertOpenAIToAnthropicTools(openAITools)
      
      expect(anthropicTools).toHaveLength(1)
      expect(anthropicTools[0].name).toBe('get_weather')
      expect(anthropicTools[0].description).toBe('Get the weather for a location')
      expect(anthropicTools[0].input_schema).toEqual({
        type: 'object',
        properties: {
          location: { type: 'string' }
        }
      })
    })
  })

  describe('convertAnthropicToOpenAITools', () => {
    it('should convert Anthropic tools to OpenAI format', () => {
      const anthropicTools: AnthropicTool[] = [
        {
          name: 'get_weather',
          description: 'Get the weather for a location',
          input_schema: {
            type: 'object',
            properties: {
              location: { type: 'string' }
            }
          }
        }
      ]

      const openAITools = convertAnthropicToOpenAITools(anthropicTools)
      
      expect(openAITools).toHaveLength(1)
      expect(openAITools[0].type).toBe('function')
      expect(openAITools[0].function.name).toBe('get_weather')
      expect(openAITools[0].function.description).toBe('Get the weather for a location')
      expect(openAITools[0].function.parameters).toEqual({
        type: 'object',
        properties: {
          location: { type: 'string' }
        }
      })
    })
  })

  describe('convertMessagesToPrompt', () => {
    it('should convert OpenAI messages to prompt format', () => {
      const messages: OpenAIMessage[] = [
        { role: 'system', content: 'You are a coding assistant.' },
        { role: 'user', content: 'Write a hello world function.' }
      ]

      const prompt = convertMessagesToPrompt(messages)
      
      expect(prompt).toBe('SYSTEM: You are a coding assistant.\n\nUSER: Write a hello world function.')
    })

    it('should convert Anthropic messages to prompt format', () => {
      const messages: AnthropicMessage[] = [
        { 
          role: 'system', 
          content: [{ type: 'text', text: 'You are a coding assistant.' }] 
        },
        { 
          role: 'user', 
          content: [{ type: 'text', text: 'Write a hello world function.' }] 
        }
      ]

      const prompt = convertMessagesToPrompt(messages)
      
      expect(prompt).toBe('SYSTEM: You are a coding assistant.\n\nUSER: Write a hello world function.')
    })

    it('should handle mixed message formats', () => {
      const messages = [
        { role: 'system', content: 'You are a coding assistant.' },
        { 
          role: 'user', 
          content: [{ type: 'text', text: 'Write a hello world function.' }] 
        }
      ] as Array<OpenAIMessage | AnthropicMessage>

      const prompt = convertMessagesToPrompt(messages)
      
      expect(prompt).toBe('SYSTEM: You are a coding assistant.\n\nUSER: Write a hello world function.')
    })
  })

  describe('parseCliOutput', () => {
    it('should parse valid JSON output', () => {
      const output = '{"id": "test-id", "choices": [{"message": {"role": "assistant", "content": "Hello!"}}]}'
      
      const parsed = parseCliOutput(output)
      
      expect(parsed).toEqual({
        id: 'test-id',
        choices: [{ message: { role: 'assistant', content: 'Hello!' } }]
      })
    })

    it('should handle non-JSON output as text response', () => {
      const output = 'Plain text response'
      
      const parsed = parseCliOutput(output)
      
      expect(parsed).toEqual({
        choices: [
          {
            message: {
              role: 'assistant',
              content: 'Plain text response'
            }
          }
        ]
      })
    })
  })
})