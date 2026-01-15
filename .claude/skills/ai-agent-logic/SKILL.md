---
name: ai-agent-logic
description: A skill for configuring OpenAI Agents SDK logic using OpenRouter (no OpenAI key). Handles agent creation, tool calling, behavior mapping, confirmation, and error handling. Always uses Context7 MCP for documentation access. Follows SDD workflow methodology.
version: 1.0.0
---

# AI Agent Logic Skill

## Purpose

The ai-agent-logic skill is designed to help users configure and implement OpenAI Agents SDK logic using OpenRouter instead of a traditional OpenAI key. It handles agent creation, tool calling, behavior mapping, confirmation responses, and error handling while following SDD methodology.

## When to Use

Use this skill when you need to:

- **Configure AI agents** for natural language task management
  - User: "Set up an agent to handle 'add task to buy groceries' command using MCP tools"
  - Assistant: Uses the skill to build and configure the OpenRouter-integrated agent logic following SDD workflow

- **Update agent behavior** for better confirmation and error handling
  - User: "Improve the agent to confirm actions and handle errors gracefully"
  - Assistant: Uses the skill to update agent behavior mapping, confirmation responses, and error handling

- **Map agent behaviors** to specific MCP tools
  - User: "Configure the agent to map 'complete task' commands to the complete_task MCP tool"
  - Assistant: Uses the skill to create proper behavior mappings for the agent

- **Integrate with OpenRouter** instead of OpenAI API directly
  - User: "Configure the agent to use OpenRouter for API calls"
  - Assistant: Uses the skill to set up OpenRouter integration for the agent

## Process Steps

1. **Analyze Agent Requirements**
   - Identify the specific agent functionality needed
   - Determine required MCP tools for integration
   - Define behavior mapping requirements

2. **Research with Context7 MCP**
   - Use Context7 MCP to access latest OpenAI Agents SDK documentation
   - Look up best practices for OpenRouter integration
   - Verify current standards for agent configuration

3. **Design Agent Configuration**
   - Define agent name, description, and instructions
   - Specify required tools and their configurations
   - Plan behavior mapping and confirmation flows

4. **Implement Agent Logic**
   - Configure OpenRouter as the API provider
   - Set up proper tool calling mechanisms
   - Implement confirmation and error handling
   - Add behavior mapping logic

5. **Validate Implementation**
   - Test agent creation and initialization
   - Verify tool calling functionality
   - Confirm error handling works correctly
   - Validate behavior mappings function as expected

6. **Review and Iterate**
   - Check against quality criteria
   - Validate with stakeholders if needed
   - Update based on feedback

## Output Format

AI agents created with this skill follow a standardized format:

```typescript
import OpenAI from "openai";

// OpenRouter configuration
const openRouterConfig = {
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
  defaultHeaders: {
    "HTTP-Referer": process.env.OPENROUTER_REFERRER,
    "X-Title": process.env.OPENROUTER_TITLE,
  },
};

// Agent creation function
export const createAgent = async () => {
  const openai = new OpenAI(openRouterConfig);

  const agent = await openai.beta.assistants.create({
    name: "Task Management Agent",
    description: "An agent that helps manage tasks using MCP tools",
    model: "your-preferred-model",
    instructions: "You are a helpful task management assistant...",
    tools: [
      // MCP tools configuration
    ],
  });

  return agent;
};

// Agent behavior mapping
export const mapAgentBehavior = (input: string) => {
  // Logic to map user input to appropriate MCP tools
  // Confirmation and error handling
};

// Tool calling handler
export const handleToolCalls = async (toolCalls: any[]) => {
  // Logic to handle tool calls and return results
};
```

## Quality Criteria

AI agents created with this skill must meet the following criteria:

- **OpenRouter Integration**: Properly configured to use OpenRouter instead of OpenAI API directly
- **Tool Calling**: Correctly integrates with MCP tools for task management
- **Behavior Mapping**: Maps user intents to appropriate actions accurately
- **Confirmation Handling**: Provides clear confirmation for user actions
- **Error Handling**: Gracefully handles errors and provides user-friendly messages
- **Security**: Properly manages API keys and sensitive information
- **Performance**: Efficient response times and minimal latency
- **Reliability**: Consistent behavior across different inputs and scenarios
- **Documentation**: Clear documentation of agent capabilities and limitations
- **Maintainability**: Well-structured code that's easy to update and extend

## Context7 MCP Integration

This skill mandates the use of Context7 MCP for:

- Accessing up-to-date documentation on OpenAI Agents SDK
- Retrieving best practices for OpenRouter integration
- Validating agent configuration patterns
- Checking tool calling implementations
- Ensuring compatibility with current MCP tool patterns