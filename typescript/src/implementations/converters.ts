import {
  OpenAIMessage,
  AnthropicMessage,
  ContentBlock,
  OpenAITool,
  AnthropicTool,
} from '../types'

/**
 * Converts an OpenAI style message to an Anthropic style message
 */
export function convertOpenAIToAnthropicMessage(message: OpenAIMessage): AnthropicMessage {
  if (typeof message.content === 'string') {
    return {
      role: message.role,
      content: [{ type: 'text', text: message.content }],
      files: message.files,
    }
  } else {
    // Message content is already in a compatible format
    return message as unknown as AnthropicMessage
  }
}

/**
 * Converts an Anthropic style message to an OpenAI style message
 */
export function convertAnthropicToOpenAIMessage(message: AnthropicMessage): OpenAIMessage {
  if (typeof message.content === 'string') {
    return message as unknown as OpenAIMessage
  } else {
    // Convert content array to string (concatenating text blocks)
    const contentBlocks = message.content as ContentBlock[]
    const textContent = contentBlocks
      .filter(block => block.type === 'text' && block.text)
      .map(block => block.text)
      .join('\n')

    return {
      role: message.role,
      content: textContent,
      files: message.files,
    }
  }
}

/**
 * Converts OpenAI style tools to Anthropic style tools
 */
export function convertOpenAIToAnthropicTools(tools: OpenAITool[]): AnthropicTool[] {
  return tools.map(tool => {
    return {
      name: tool.function.name,
      description: tool.function.description,
      input_schema: tool.function.parameters || {},
    }
  })
}

/**
 * Converts Anthropic style tools to OpenAI style tools
 */
export function convertAnthropicToOpenAITools(tools: AnthropicTool[]): OpenAITool[] {
  return tools.map(tool => {
    return {
      type: 'function',
      function: {
        name: tool.name,
        description: tool.description,
        parameters: tool.input_schema,
      },
    }
  })
}

/**
 * Converts an array of messages to a single prompt string for the CLI
 */
export function convertMessagesToPrompt(messages: Array<OpenAIMessage | AnthropicMessage>): string {
  // Handle the case where we might receive either OpenAI or Anthropic style messages
  return messages
    .map(message => {
      const role = message.role.toUpperCase()
      
      // Handle different content formats
      let content: string
      if (typeof message.content === 'string') {
        content = message.content
      } else {
        // Convert Anthropic's content array to string
        content = (message.content as ContentBlock[])
          .filter(block => block.type === 'text' && block.text)
          .map(block => block.text)
          .join('\n')
      }
      
      return `${role}: ${content}`
    })
    .join('\n\n')
}

/**
 * Parses CLI output in JSON format to appropriate completion response
 */
export function parseCliOutput<T>(output: string): T {
  try {
    return JSON.parse(output) as T
  } catch (error) {
    // If we can't parse as JSON, return text output in a structured format
    return {
      choices: [
        {
          message: {
            role: 'assistant',
            content: output.trim(),
          },
        },
      ],
    } as unknown as T
  }
}