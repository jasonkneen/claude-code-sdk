import { ClaudeCode } from '../index'

// Example usage of the Claude Code SDK

async function main(): Promise<void> {
  // Create a client
  const claude = new ClaudeCode({
    apiKey: process.env.ANTHROPIC_API_KEY,
  })

  try {
    console.log('Using OpenAI-style chat completions API:')
    const completion = await claude.chat.completions.create({
      model: 'claude-code',
      messages: [
        { role: 'user', content: 'Write a function to calculate the Fibonacci sequence in TypeScript' }
      ],
      max_tokens: 1000,
    })

    console.log(completion.choices[0].message.content)
    console.log('\n---\n')

    console.log('Using Anthropic-style messages API:')
    const message = await claude.messages.create({
      model: 'claude-code',
      messages: [
        { 
          role: 'user', 
          content: [{ 
            type: 'text', 
            text: 'Write a function to sort an array using quicksort in TypeScript' 
          }] 
        }
      ],
      max_tokens: 1000,
    })

    if (Array.isArray(message.content)) {
      console.log(message.content[0].text)
    }
    console.log('\n---\n')

    console.log('Using session management:')
    const session = await claude.sessions.create({
      messages: [
        { role: 'user', content: 'Let\'s create a simple Express.js API' }
      ]
    })

    console.log('Session created with ID:', session.id)
    
    const sessionResponse = await session.continue({
      messages: [
        { role: 'user', content: 'Now add a route to get a list of users' }
      ]
    })

    console.log('Session response:')
    // Handle both OpenAI and Anthropic response formats
    if ('choices' in sessionResponse) {
      console.log(sessionResponse.choices[0].message.content)
    } else if ('content' in sessionResponse && Array.isArray(sessionResponse.content)) {
      console.log(sessionResponse.content[0].text)
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

// Execute the example if this file is run directly
if (require.main === module) {
  main().catch(console.error)
}

export default main