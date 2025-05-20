import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ClaudeCode } from '../index'
import { ClaudeCliExecutor } from '../implementations/cli'

// Mock the CLI executor class
vi.mock('../implementations/cli', () => {
  return {
    ClaudeCliExecutor: vi.fn().mockImplementation(() => {
      return {
        execute: vi.fn().mockResolvedValue('{"id": "mock-id", "choices": [{"message": {"role": "assistant", "content": "Mock response"}}]}'),
        executeStream: vi.fn(() => {
          const { Readable } = require('stream')
          const stream = new Readable({
            read() {}
          })
          
          // Simulate data events
          setTimeout(() => {
            stream.push(Buffer.from('{"id": "chunk-1", "choices": [{"delta": {"content": "Mock"}}]}'))
            stream.push(Buffer.from('{"id": "chunk-2", "choices": [{"delta": {"content": " response"}}]}'))
            stream.push(null) // End the stream
          }, 0)
          
          return stream
        })
      }
    })
  }
})

describe('ClaudeCode client', () => {
  let claude: ClaudeCode

  beforeEach(() => {
    claude = new ClaudeCode({ apiKey: 'test-api-key' })
  })

  describe('Client initialization', () => {
    it('should create a client instance', () => {
      expect(claude).toBeInstanceOf(ClaudeCode)
      expect(claude.chat.completions).toBeDefined()
      expect(claude.messages).toBeDefined()
      expect(claude.sessions).toBeDefined()
      expect(claude.tools).toBeDefined()
    })

    it('should initialize with provided options', () => {
      const customClient = new ClaudeCode({
        apiKey: 'custom-key',
        cliPath: 'custom-path',
        timeout: 60000,
      })
      
      expect(customClient).toBeInstanceOf(ClaudeCode)
    })
  })

  describe('OpenAI-style API', () => {
    it('should have chat.completions.create method', () => {
      expect(typeof claude.chat.completions.create).toBe('function')
    })
    
    it('should have chat.completions.createStream method', () => {
      expect(typeof claude.chat.completions.createStream).toBe('function')
    })

    it('should call the CLI executor when using create', async () => {
      const response = await claude.chat.completions.create({
        model: 'claude-code',
        messages: [{ role: 'user', content: 'Test prompt' }]
      })

      expect(response).toBeDefined()
      expect(response.id).toBe('mock-id')
      expect(response.choices[0].message.content).toBe('Mock response')
    })
  })

  describe('Anthropic-style API', () => {
    it('should have messages.create method', () => {
      expect(typeof claude.messages.create).toBe('function')
    })
    
    it('should have messages.createStream method', () => {
      expect(typeof claude.messages.createStream).toBe('function')
    })

    it('should call the CLI executor when using create', async () => {
      const response = await claude.messages.create({
        model: 'claude-code',
        messages: [{ 
          role: 'user', 
          content: [{ type: 'text', text: 'Test prompt' }] 
        }]
      })

      expect(response).toBeDefined()
    })
  })

  describe('Session management', () => {
    it('should have sessions.create method', () => {
      expect(typeof claude.sessions.create).toBe('function')
    })
    
    it('should have sessions.resume method', () => {
      expect(typeof claude.sessions.resume).toBe('function')
    })

    it('should create a session with an ID', async () => {
      const session = await claude.sessions.create({
        messages: [{ role: 'user', content: 'Start session' }]
      })

      expect(session).toBeDefined()
      expect(session.id).toBeDefined()
    })
  })

  describe('Tools', () => {
    it('should have tools.create method', () => {
      expect(typeof claude.tools.create).toBe('function')
    })
    
    it('should have tools.get method', () => {
      expect(typeof claude.tools.get).toBe('function')
    })
    
    it('should have tools.list method', () => {
      expect(typeof claude.tools.list).toBe('function')
    })

    it('should register a tool and retrieve it', async () => {
      const tool = await claude.tools.create({
        name: 'test-tool',
        description: 'A test tool',
        input_schema: { type: 'object', properties: { test: { type: 'string' } } }
      })

      expect(tool).toBeDefined()
      expect(tool.name).toBe('test-tool')
      
      const retrievedTool = claude.tools.get('test-tool')
      expect(retrievedTool).toBeDefined()
      expect(retrievedTool?.name).toBe('test-tool')
      
      const allTools = claude.tools.list()
      expect(allTools).toHaveLength(1)
      expect(allTools[0].name).toBe('test-tool')
    })
  })
})