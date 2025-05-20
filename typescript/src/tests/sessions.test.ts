import { describe, it, expect, vi, beforeEach } from 'vitest'
import { Session, Sessions } from '../client/sessions'
import { BaseClient } from '../client/base'

// Mock the BaseClient class
vi.mock('../client/base', () => {
  return {
    BaseClient: vi.fn().mockImplementation(() => {
      return {
        executeCommand: vi.fn().mockImplementation((params) => {
          if (params.resume) {
            return Promise.resolve('{"id": "resumed-session", "choices": [{"message": {"role": "assistant", "content": "Resumed session"}}]}')
          } else {
            return Promise.resolve('{"id": "new-session", "choices": [{"message": {"role": "assistant", "content": "New session"}}]}')
          }
        })
      }
    })
  }
})

describe('Sessions', () => {
  let mockClient: BaseClient
  let sessions: Sessions
  
  beforeEach(() => {
    mockClient = new BaseClient()
    sessions = new Sessions(mockClient)
  })
  
  describe('create', () => {
    it('should create a new session with messages', async () => {
      const session = await sessions.create({
        messages: [{ role: 'user', content: 'Start session' }]
      })
      
      expect(session).toBeInstanceOf(Session)
      expect(session.id).toBeDefined()
      expect(mockClient.executeCommand).toHaveBeenCalled()
      
      const params = (mockClient.executeCommand as any).mock.calls[0][0]
      expect(params.prompt).toBeDefined()
      expect(params.outputFormat).toBe('json')
    })
    
    it('should create a session with a generated ID if not present in response', async () => {
      // Override mock to return a response without ID
      (mockClient.executeCommand as any).mockImplementationOnce(() => {
        return Promise.resolve('{"choices": [{"message": {"role": "assistant", "content": "No ID"}}]}')
      })
      
      const session = await sessions.create({
        messages: [{ role: 'user', content: 'Start session' }]
      })
      
      expect(session).toBeInstanceOf(Session)
      expect(session.id).toBeDefined()
      expect(session.id).toContain('session_')
    })
  })
  
  describe('resume', () => {
    it('should resume an existing session by ID', async () => {
      const sessionId = 'test-session-id'
      const session = await sessions.resume(sessionId)
      
      expect(session).toBeInstanceOf(Session)
      expect(session.id).toBe(sessionId)
      expect(mockClient.executeCommand).toHaveBeenCalled()
      
      const params = (mockClient.executeCommand as any).mock.calls[0][0]
      expect(params.resume).toBe(sessionId)
      expect(params.outputFormat).toBe('json')
    })
  })
})

describe('Session', () => {
  let mockClient: BaseClient
  let session: Session
  const sessionId = 'test-session-id'
  const initialMessages = [{ role: 'user' as const, content: 'Initial message' }]
  
  beforeEach(() => {
    mockClient = new BaseClient()
    session = new Session(sessionId, mockClient, initialMessages)
  })
  
  describe('continue', () => {
    it('should continue a session with new messages', async () => {
      const response = await session.continue({
        messages: [{ role: 'user', content: 'Continue session' }]
      })
      
      expect(response).toBeDefined()
      expect(mockClient.executeCommand).toHaveBeenCalled()
      
      const params = (mockClient.executeCommand as any).mock.calls[0][0]
      expect(params.prompt).toBeDefined()
      expect(params.resume).toBe(sessionId)
      expect(params.outputFormat).toBe('json')
    })
  })
  
  describe('getMessages', () => {
    it('should return all messages in the session', () => {
      const messages = session.getMessages()
      
      expect(messages).toEqual(initialMessages)
      
      // Continue the session to add more messages
      session.continue({
        messages: [{ role: 'user', content: 'Continue session' }]
      })
      
      const updatedMessages = session.getMessages()
      expect(updatedMessages).toHaveLength(2)
      expect(updatedMessages[0]).toEqual(initialMessages[0])
      expect(updatedMessages[1]).toEqual({ role: 'user', content: 'Continue session' })
    })
    
    it('should return a copy of the messages array', () => {
      const messages = session.getMessages()
      
      // Modify the returned array
      messages.push({ role: 'user', content: 'New message' })
      
      // Original messages in the session should not be affected
      const internalMessages = session.getMessages()
      expect(internalMessages).toHaveLength(1)
      expect(internalMessages[0]).toEqual(initialMessages[0])
    })
  })
})