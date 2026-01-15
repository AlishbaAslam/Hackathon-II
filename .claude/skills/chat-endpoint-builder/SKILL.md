---
name: chat-endpoint-builder
description: A skill for implementing stateless FastAPI chat endpoint (/api/{user_id}/chat), history fetch/store from Neon DB, agent invocation with OpenRouter, response handling. Always uses Context7 MCP for documentation access. Follows SDD workflow methodology.
version: 1.0.0
---

# Chat Endpoint Builder Skill

## Purpose

The chat-endpoint-builder skill is designed to help users implement stateless FastAPI chat endpoints that handle conversation history with Neon DB, invoke AI agents via OpenRouter, and properly handle responses. It ensures proper user isolation, stateless design, and follows SDD methodology.

## When to Use

Use this skill when you need to:

- **Implement the main chat endpoint** for the chatbot
  - User: "Create the POST /api/{user_id}/chat endpoint with history persistence"
  - Assistant: Uses the skill to implement the stateless chat endpoint following SDD workflow

- **Update the endpoint** to include OpenRouter integration
  - User: "Update the chat endpoint to use OpenRouter and handle errors gracefully"
  - Assistant: Uses the skill to update the endpoint with OpenRouter configuration and error handling

- **Handle conversation history** with Neon DB
  - User: "Implement conversation history fetch and store functionality"
  - Assistant: Uses the skill to ensure proper DB persistence and retrieval

- **Ensure proper user isolation** in the endpoint
  - User: "Verify that the chat endpoint properly isolates user conversations"
  - Assistant: Uses the skill to implement and validate user_id-based isolation

## Process Steps

1. **Analyze Endpoint Requirements**
   - Identify the specific endpoint functionality needed
   - Determine the route pattern (/api/{user_id}/chat)
   - Define history fetch/store requirements
   - Specify agent invocation needs

2. **Research with Context7 MCP**
   - Use Context7 MCP to access latest FastAPI documentation
   - Look up best practices for stateless endpoint design
   - Verify current standards for DB integration with Neon
   - Check OpenRouter integration patterns

3. **Design Endpoint Structure**
   - Define route parameters and request/response schemas
   - Plan history fetch and store mechanisms
   - Design agent invocation flow
   - Plan response handling and error responses

4. **Implement Endpoint Logic**
   - Create stateless FastAPI route
   - Implement user_id validation and isolation
   - Add Neon DB integration for history
   - Integrate OpenRouter agent invocation
   - Add proper response handling

5. **Validate Implementation**
   - Test endpoint with different user_ids
   - Verify history persistence works correctly
   - Confirm agent invocation functions properly
   - Validate error handling paths

6. **Review and Iterate**
   - Check against quality criteria
   - Validate with stakeholders if needed
   - Update based on feedback

## Output Format

Chat endpoints created with this skill follow a standardized format:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    messages: List[Message]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Stateless chat endpoint that handles conversation history
    and invokes AI agents via OpenRouter.
    """
    # Validate user_id
    # Fetch conversation history from Neon DB
    # Invoke agent via OpenRouter
    # Store new messages in DB
    # Return response
    pass

# Additional helper functions for:
# - History fetch/store from Neon DB
# - OpenRouter agent invocation
# - Response formatting
# - Error handling
```

## Quality Criteria

Chat endpoints created with this skill must meet the following criteria:

- **Statelessness**: Endpoint maintains no internal state between requests
- **User Isolation**: Properly isolates conversations by user_id
- **DB Persistence**: Correctly stores and retrieves conversation history from Neon DB
- **OpenRouter Integration**: Properly invokes AI agents via OpenRouter API
- **Security**: Validates user permissions and prevents unauthorized access
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Response Formatting**: Consistent response structure with proper schema
- **Performance**: Efficient database queries and minimal response latency
- **Scalability**: Designed to handle multiple concurrent users
- **Maintainability**: Clean, well-documented code that's easy to update

## Context7 MCP Integration

This skill mandates the use of Context7 MCP for:

- Accessing up-to-date documentation on FastAPI
- Retrieving best practices for stateless endpoint design
- Validating Neon DB integration patterns
- Checking OpenRouter API usage guidelines
- Ensuring compatibility with current async Python patterns