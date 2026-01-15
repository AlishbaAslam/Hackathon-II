---
name: chatbot-spec-writer
description: A skill for writing, validating, and updating specifications for AI-powered chatbot projects covering overview, features, API endpoints, MCP tools, agent behavior, conversation flow, and database models. Always uses Context7 MCP for latest documentation access and updates. Follows SDD workflow methodology.
version: 1.0.0
---

# Chatbot Specification Writer Skill

## Purpose

The chatbot-spec-writer skill is designed to help users create, validate, and update comprehensive specifications for AI-powered chatbot projects. It ensures specifications are complete, consistent, and aligned with the Spec-Driven Development (SDD) methodology.

## When to Use

Use this skill when you need to:

- **Create initial specifications** for a new chatbot project
  - User: "I need to define specifications for an AI chatbot that handles customer support"
  - Assistant: Uses the skill to create overview, features, API endpoints, and database model specs

- **Update existing specifications** to reflect new requirements
  - User: "Update the API endpoint specs to include new conversation features"
  - Assistant: Uses the skill to modify existing API specifications while maintaining consistency

- **Validate specifications** for completeness and consistency
  - User: "Review the conversation flow specifications to ensure they're complete"
  - Assistant: Uses the skill to check specifications against quality criteria

- **Align specifications** with project requirements
  - User: "Ensure the MCP tools spec enforces user isolation via JWT"
  - Assistant: Uses the skill to validate and update the MCP tools specification

## Process Steps

1. **Gather Requirements**
   - Identify the specific aspect of the chatbot that needs specification
   - Determine the target audience for the specification
   - Collect any existing related specifications

2. **Research with Context7 MCP**
   - Use Context7 MCP to access latest documentation
   - Look up best practices for the specific component
   - Verify current standards and patterns

3. **Draft Specification**
   - Follow established template structure
   - Include clear user stories and acceptance criteria
   - Document edge cases and error scenarios

4. **Validate Completeness**
   - Check that all required sections are filled
   - Ensure consistency with other related specs
   - Verify technical feasibility

5. **Review and Iterate**
   - Check against quality criteria
   - Validate with stakeholders if needed
   - Update based on feedback

## Output Format

Specifications created with this skill follow a standardized format:

```markdown
# [Component Name] Specification

## Overview
Brief description of the component and its purpose in the chatbot system.

## Features
- Detailed feature requirements with priority levels (P1, P2, etc.)
- User stories with acceptance criteria
- Functional and non-functional requirements

## API Endpoints (if applicable)
- Endpoint paths and HTTP methods
- Request/response schemas
- Authentication requirements
- Error response formats

## Database Models (if applicable)
- Entity relationships
- Field definitions with types and constraints
- Indexing requirements
- Data validation rules

## MCP Tools (if applicable)
- Tool definitions with parameters
- Security requirements (user isolation)
- Error handling patterns

## Agent Behavior
- Conversation flow diagrams
- Response patterns
- Confirmation and error handling
- Integration with external systems

## Edge Cases & Error Scenarios
- Error conditions and responses
- Timeout handling
- Invalid input handling

## Validation Criteria
- Acceptance tests
- Performance requirements
- Security checks
```

## Quality Criteria

Specifications created with this skill must meet the following criteria:

- **Completeness**: All required sections are filled with sufficient detail
- **Consistency**: Aligns with other project specifications and architectural decisions
- **Clarity**: Written in clear, unambiguous language suitable for the target audience
- **Feasibility**: Technically achievable within project constraints
- **Testability**: Includes verifiable acceptance criteria
- **Maintainability**: Structured for easy updates and modifications
- **Security**: Addresses authentication, authorization, and data protection requirements
- **Performance**: Defines appropriate performance expectations
- **Error Handling**: Covers error scenarios and recovery procedures
- **Integration**: Specifies how components interact with other parts of the system

## Context7 MCP Integration

This skill mandates the use of Context7 MCP for:

- Accessing up-to-date documentation on AI chatbot frameworks
- Retrieving best practices for conversation design
- Validating API specification formats
- Checking database modeling standards
- Ensuring compatibility with current MCP tool patterns