---
id: PHR-002-ai-chatbot-plan
title: "AI Chatbot Planning & Architecture"
stage: plan
feature: "ai-chatbot"
created: 2026-01-14T14:35:00Z
status: completed
tags: [planning, architecture, ai, chatbot, mcp, openrouter]
---

# AI Chatbot Planning & Architecture

## Original Prompt

Phase-III Todo AI Chatbot - Planning for Conversational Interface & Integration

Revise the existing plan based on updated spec: Align all chatbot components to integrate with Phase-II app (right-side Chat Widget, stateless chat endpoint /api/{user_id}/chat, OpenAI Agents SDK via OpenRouter, MCP tools, conversation persistence in Neon DB). Update architecture, contracts, data-model, quickstart, and research to enforce stateless design, user isolation, tool calling.

Create:
* Updated architecture sketch with Chat Widget, chat endpoint, agent runner, MCP server, DB integration
* Revised folder structure if needed (e.g., /frontend/chat/, /backend/chat/)
* Updated section structure for specs and code
* Research on OpenRouter integration best practices (no OpenAI key, AsyncOpenAI client)
* Quality validation with ownership tests and conversation resumption

Decisions:
* AI Framework: OpenAI Agents SDK via OpenRouter (tradeoffs: cost-free vs limited models)
* Stateless Design: DB persistence for conversations (tradeoffs: scalability vs simple sessions)
* Frontend: OpenAI ChatKit widget (tradeoffs: easy integration vs custom UI)

Testing strategy:
* Update to test conversation resumption (after server restart)
* Ownership verification in all chat tests (403 on mismatch)
* Natural language command testing (confirmation, errors)
* OpenRouter model calls validation (e.g., deepseek/deepseek-r1-0528:free)

Technical details:
* Use concurrent research for OpenRouter + MCP SDK
* Phased: Update DB models → MCP tools → Agent logic → Chat endpoint → ChatKit UI
* Use Context7 MCP for all doc access/updates

Generate updated plan.md, contracts/*.yaml, etc. inside /specs/phase-III-chatbot/.

## Response Summary

Successfully completed the implementation plan for the Phase-III Todo AI Chatbot. Created the following artifacts:

1. **plan.md**: Comprehensive implementation plan with architecture, constitution check, research tasks, and phased implementation
2. **research.md**: Detailed research findings addressing OpenRouter integration, MCP SDK patterns, and ChatKit deployment
3. **data-model.md**: Complete data model specification for Conversation and Message entities
4. **contracts/chat-api.openapi.yaml**: OpenAPI specification for the chat API endpoint
5. **quickstart.md**: Implementation and deployment guide with environment setup and testing instructions

The plan addresses all key decisions:
- OpenRouter integration using AsyncOpenAI client with deepseek/deepseek-r1-0528:free model
- Standalone MCP server architecture for proper service separation
- ChatKit domain configuration with production deployment requirements
- Stateless design with database persistence for scalability
- User isolation enforcement through JWT validation and database queries

## Key Decisions Made

1. **AI Framework**: OpenAI Agents SDK via OpenRouter for cost-free operations
2. **Architecture**: Standalone MCP server with clear service boundaries
3. **Frontend**: ChatKit widget for rapid integration and maintained UI
4. **Data Persistence**: Database-stored conversations for stateless scalability
5. **Security**: JWT-based user isolation with database-level access controls

## Status

Planning phase completed successfully. All required artifacts created and linked. Ready for the next phase (tasks generation and implementation).