---
name: mcp-tool-designer
description: A skill for designing and implementing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) using the Official MCP SDK, with statelessness, user_id isolation, and DB persistence. Always uses Context7 MCP for latest specifications. Follows SDD workflow methodology.
version: 1.0.0
---

# MCP Tool Designer Skill

## Purpose

The mcp-tool-designer skill is designed to help users create, validate, and implement MCP (Model Context Protocol) tools for task management operations. It ensures tools are stateless, properly isolate user data, and persist to databases while following SDD methodology.

## When to Use

Use this skill when you need to:

- **Design new MCP tools** for task management functionality
  - User: "Create MCP tools for add_task, list_tasks, complete_task, delete_task, and update_task"
  - Assistant: Uses the skill to design and implement the required MCP tools following SDD workflow

- **Update existing MCP tools** to meet new requirements
  - User: "Modify the MCP tools to include additional validation and error handling"
  - Assistant: Uses the skill to update existing tools while ensuring compliance with requirements

- **Validate MCP tool specifications** for completeness and consistency
  - User: "Review the MCP tool specs to ensure they enforce user isolation via JWT"
  - Assistant: Uses the skill to check specifications against quality criteria

- **Implement MCP tools** with proper statelessness and user isolation
  - User: "Implement the list_tasks MCP tool with proper user_id filtering"
  - Assistant: Uses the skill to ensure proper implementation with user isolation

## Process Steps

1. **Analyze Requirements**
   - Identify the specific MCP tool to be designed or updated
   - Determine the parameters and return types needed
   - Define user isolation requirements

2. **Research with Context7 MCP**
   - Use Context7 MCP to access latest MCP SDK documentation
   - Look up best practices for MCP tool design
   - Verify current standards and patterns for stateless tools

3. **Design Tool Schema**
   - Define the JSON schema for parameters
   - Specify return types and possible error conditions
   - Include user_id isolation mechanisms

4. **Implement Tool Logic**
   - Write stateless implementation using MCP SDK
   - Implement user_id validation and isolation
   - Add database persistence logic
   - Include proper error handling

5. **Validate Implementation**
   - Check that tool is truly stateless
   - Verify user_id isolation works correctly
   - Ensure database persistence functions properly
   - Test error handling paths

6. **Review and Iterate**
   - Check against quality criteria
   - Validate with stakeholders if needed
   - Update based on feedback

## Output Format

MCP tools created with this skill follow a standardized format:

```typescript
import { Tool } from "@modelcontextprotocol/sdk";

export const createAddTaskTool = (): Tool => {
  return {
    // Tool definition following MCP specification
    // Stateless implementation
    // User_id isolation
    // DB persistence
  };
};

export const createListTasksTool = (): Tool => {
  return {
    // Tool definition following MCP specification
    // Stateless implementation
    // User_id isolation
    // DB persistence
  };
};

export const createCompleteTaskTool = (): Tool => {
  return {
    // Tool definition following MCP specification
    // Stateless implementation
    // User_id isolation
    // DB persistence
  };
};

export const createDeleteTaskTool = (): Tool => {
  return {
    // Tool definition following MCP specification
    // Stateless implementation
    // User_id isolation
    // DB persistence
  };
};

export const createUpdateTaskTool = (): Tool => {
  return {
    // Tool definition following MCP specification
    // Stateless implementation
    // User_id isolation
    // DB persistence
  };
};
```

## Quality Criteria

MCP tools created with this skill must meet the following criteria:

- **Statelessness**: Tools maintain no internal state between invocations
- **User Isolation**: All operations properly filter by user_id to prevent data leakage
- **Database Persistence**: Proper integration with database for storing/retrieving data
- **Security**: Validates user permissions and prevents unauthorized access
- **Error Handling**: Comprehensive error handling with appropriate messages
- **Parameter Validation**: Proper validation of all input parameters
- **Documentation**: Clear documentation of parameters and return values
- **Performance**: Efficient database queries and minimal resource usage
- **Consistency**: Follows MCP specification and SDK best practices
- **Testability**: Designed to be easily testable with unit and integration tests

## Context7 MCP Integration

This skill mandates the use of Context7 MCP for:

- Accessing up-to-date documentation on MCP SDK
- Retrieving best practices for tool design
- Validating MCP specification compliance
- Checking database integration patterns
- Ensuring compatibility with current MCP tool patterns