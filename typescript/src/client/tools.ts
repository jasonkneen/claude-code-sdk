import { BaseClient } from './base'
import { AnthropicTool } from '../types'

// Interface for tool creation
export interface ToolCreateParams {
  name: string
  description?: string
  input_schema: Record<string, unknown>
}

// Class for tools management
export class Tools {
  private client: BaseClient
  private registeredTools: Map<string, AnthropicTool>

  constructor(client: BaseClient) {
    this.client = client
    this.registeredTools = new Map()
  }

  /**
   * Register a new tool for later use
   */
  async create(params: ToolCreateParams): Promise<AnthropicTool> {
    // Create a new tool definition
    const tool: AnthropicTool = {
      name: params.name,
      description: params.description,
      input_schema: params.input_schema,
    }

    // Store the tool for later use
    this.registeredTools.set(params.name, tool)
    
    return tool
  }

  /**
   * Get a tool by name
   */
  get(name: string): AnthropicTool | undefined {
    return this.registeredTools.get(name)
  }

  /**
   * List all registered tools
   */
  list(): AnthropicTool[] {
    return Array.from(this.registeredTools.values())
  }
}