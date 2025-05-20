import { describe, it, expect, vi } from 'vitest'
import { ClaudeCliExecutor } from '../implementations/cli'
import { Readable } from 'stream'

describe('ClaudeCliExecutor', () => {
  describe('buildArgs', () => {
    it('should build arguments array with the correct parameters', () => {
      const executor = new ClaudeCliExecutor({ cliPath: 'claude-code' })
      
      // Access the private method for testing
      const buildArgs = (executor as any)['buildArgs'].bind(executor)
      
      // Test basic parameters
      const args1 = buildArgs({
        prompt: 'Test prompt',
        outputFormat: 'json'
      })
      
      expect(args1).toContain('-p')
      expect(args1).toContain('Test prompt')
      expect(args1).toContain('--output-format')
      expect(args1).toContain('json')
      
      // Test with system prompt
      const args2 = buildArgs({
        prompt: 'Test prompt',
        systemPrompt: 'You are a helpful assistant',
        outputFormat: 'json'
      })
      
      expect(args2).toContain('--system-prompt')
      expect(args2).toContain('You are a helpful assistant')
      
      // Test with quote escaping (quotes are not escaped when using spawn with args)
      const args3 = buildArgs({
        prompt: 'Test "quoted" prompt',
        outputFormat: 'json'
      })
      
      expect(args3).toContain('Test "quoted" prompt')
      
      // Test with allowed tools
      const args4 = buildArgs({
        prompt: 'Test prompt',
        allowedTools: ['filesystem', 'web-search']
      })
      
      expect(args4).toContain('--allowedTools')
      expect(args4).toContain('filesystem,web-search')
      
      // Test with session continuation
      const args5 = buildArgs({
        continue: true,
        prompt: 'Continue session'
      })
      
      expect(args5).toContain('--continue')
      
      // Test with session resumption
      const args6 = buildArgs({
        resume: 'abc123',
        prompt: 'Resume session'
      })
      
      expect(args6).toContain('--resume')
      expect(args6).toContain('abc123')
    })
  })
})