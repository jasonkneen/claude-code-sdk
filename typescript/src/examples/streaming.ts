import { ClaudeCode } from '../index'

// Example of streaming responses with Claude Code SDK

async function streamExample(): Promise<void> {
  // Create a client
  const claude = new ClaudeCode({
    apiKey: process.env.ANTHROPIC_API_KEY,
  })

  try {
    console.log('Streaming with OpenAI-style API:')
    console.log('--------------------------------')
    
    // OpenAI-style streaming
    const openaiStream = await claude.chat.completions.createStream({
      model: 'claude-code',
      messages: [
        { role: 'user', content: 'Write a React component for a to-do list with TypeScript' }
      ]
    })

    console.log('Response:')
    for await (const chunk of openaiStream) {
      if (chunk.choices && chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content)
      }
    }
    
    console.log('\n\n')
    console.log('Streaming with Anthropic-style API:')
    console.log('---------------------------------')
    
    // Anthropic-style streaming
    const anthropicStream = await claude.messages.createStream({
      model: 'claude-code',
      messages: [
        { 
          role: 'user', 
          content: [{ 
            type: 'text', 
            text: 'Write a TypeScript utility for handling API errors' 
          }] 
        }
      ]
    })

    console.log('Response:')
    for await (const chunk of anthropicStream) {
      if (chunk.type === 'content_block_delta' && chunk.delta?.text) {
        process.stdout.write(chunk.delta.text)
      }
    }
    
    console.log('\n')
    
  } catch (error) {
    console.error('Error:', error)
  }
}

// Execute the example if this file is run directly
if (require.main === module) {
  streamExample().catch(console.error)
}

export default streamExample