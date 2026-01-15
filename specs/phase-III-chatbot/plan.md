# Implementation Plan: Phase-III Todo AI Chatbot

**Feature**: Phase-III Todo AI Chatbot - Planning for Integration into Existing Phase-II App
**Spec Reference**: [spec.md](./spec.md)
**Created**: 2026-01-14
**Planned By**: Claude Code

## Technical Context

### Architecture Components
- **Frontend Integration**: Add Chat Widget (floating right-side button/icon) in existing layout/components, click opens ChatKit chat interface
- **Backend Integration**: Add new `/api/{user_id}/chat` endpoint in existing backend, use OpenRouter (no OpenAI key) for agent logic
- **Database**: Add Conversation and Message models/tables to existing Neon DB (Task table remains unchanged)
- **Authentication**: Reuse Better Auth JWT for chat endpoint (user_id isolation)
- **MCP Tools**: Add 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) to existing backend
- **All changes in same repo**: frontend/, backend/, specs/phase-III-chatbot/
- **AI Framework**: OpenAI Agents SDK via OpenRouter (no OpenAI key required)

### Technology Stack
- **Frontend**: Next.js 16+, React, ChatKit UI
- **Backend**: Python 3.13+, FastAPI 0.115+, AsyncOpenAI client
- **AI**: OpenAI Agents SDK via OpenRouter
- **MCP**: Official MCP SDK
- **Database**: SQLModel 0.0.24+, Neon PostgreSQL
- **Authentication**: Better Auth with JWT

### Key Decisions Made
- OpenRouter model selection: deepseek/deepseek-r1-0528:free for cost-free operations
- MCP server hosting: Integrated within existing backend (not standalone) to maintain single codebase
- ChatKit domain configuration: Domain allowlist required for production deployment
- Integration approach: Direct integration into existing Phase-II app structure

## Architecture Updates

- **Integration Architecture**: Chat Widget → ChatKit UI → Existing FastAPI server → /api/{user_id}/chat endpoint
- **Processing Architecture**: Endpoint → OpenRouter Agent (via OpenAI Agents SDK) → MCP Server (tools) → Neon DB (tasks + conversations + messages)
- **State Management**: Stateless server design with all state stored in database
- **Component Integration**: MCP tools integrated directly into existing backend (not standalone server)

## Research

### OpenRouter Integration Research
- **Objective**: Integrate AsyncOpenAI client with OpenRouter for cost-free AI operations
- **Findings**: OpenRouter supports deepseek/deepseek-r1-0528:free model with standard OpenAI API compatibility
- **Implementation**: Configure AsyncOpenAI client with OpenRouter base_url and API key from environment variables

### OpenAI ChatKit Domain Configuration Research
- **Objective**: Set up domain allowlist for ChatKit frontend deployment
- **Process**: Deploy frontend first to get production URL, add to OpenAI's domain allowlist, obtain NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- **Configuration**: Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY environment variable for hosted ChatKit

### Floating Right-Side Widget Research
- **Objective**: Implement non-intrusive, responsive chat widget in Next.js application
- **Best Practices**: Use fixed positioning with z-index, responsive design for all screen sizes, accessibility compliance (WCAG 2.1 AA)
- **Implementation**: Create floating button that slides open chat interface when clicked

## Constitution Check

### SDD Compliance
- ✅ Feature originates from approved specification in `spec.md`
- ✅ Follows Spec-Driven Development methodology
- ✅ Architecture decisions documented with trade-offs

### Progressive Evolution
- ✅ Builds upon existing Phase-II infrastructure without rewrite
- ✅ Adds new functionality incrementally
- ✅ Maintains backward compatibility with existing features

### Cloud Native Principles
- ✅ Stateless design with externalized state in Neon DB
- ✅ Horizontal scaling enabled through JWT-based authentication
- ✅ Integrated services within existing backend (not separate microservices)

### Security & Privacy
- ✅ User isolation enforced through JWT tokens
- ✅ Data access restricted by user_id in all operations
- ✅ Secure authentication with Better Auth

## Testing Strategy

### Unit Tests for MCP Tools
- Test each MCP tool individually for proper functionality
- Validate user_id isolation with 403 error responses for unauthorized access
- Test parameter validation and error handling for each tool
- Verify proper database operations for each tool

### Integration Tests for Chat Endpoint
- Test conversation history persistence and retrieval
- Validate JWT authentication and user_id extraction
- Verify conversation resumption after server restart
- Test stateless operation with proper state management

### End-to-End Tests for Natural Language Commands
- Test all specified natural language commands for correct tool invocation
- Validate confirmation responses for all successful operations
- Test error handling for invalid commands and non-existent tasks
- Verify proper user isolation across different user accounts

## Gates

### Gate 1: Architecture Feasibility
✅ OpenAI Agents SDK can work with OpenRouter via AsyncOpenAI client
✅ MCP tools can be integrated within existing FastAPI backend (not standalone)
✅ ChatKit can be embedded as right-side widget in existing frontend
✅ Direct integration into existing Phase-II app structure is feasible

### Gate 2: Technology Compatibility
✅ All listed technologies are compatible with each other
✅ OpenRouter supports required AI model (deepseek/deepseek-r1-0528:free)
✅ Better Auth JWT can be integrated with FastAPI endpoints
✅ MCP SDK can be integrated within existing backend structure

### Gate 3: User Isolation
✅ All operations will be validated against user_id from JWT
✅ MCP tools will enforce user isolation within existing backend
✅ Database queries will include user_id filters for all operations

## Phase 0: Research & Unknown Resolution

### Completed Research Tasks
- **OpenRouter Integration**: AsyncOpenAI client configured for OpenRouter with deepseek/deepseek-r1-0528:free model
- **MCP SDK Implementation**: Standalone MCP server architecture selected with proper service boundaries
- **ChatKit Deployment**: Domain allowlist process documented with NEXT_PUBLIC_OPENAI_DOMAIN_KEY configuration

For detailed findings, see [research.md](./research.md)

## Phase 1: Design & Contracts

### Completed Design Artifacts
- **Data Model**: See [data-model.md](./data-model.md) for complete entity definitions
- **API Contracts**: See [contracts/chat-api.openapi.yaml](./contracts/chat-api.openapi.yaml) for OpenAPI specification
- **Quickstart Guide**: See [quickstart.md](./quickstart.md) for implementation and deployment instructions

### Key Design Elements
- **Conversation Entity**: user_id, id, created_at, updated_at
- **Message Entity**: user_id, id, conversation_id, role, content, created_at
- **API Endpoint**: POST `/api/{user_id}/chat` with JWT authentication
- **MCP Tools**: 5 task operations with user_id isolation

## Implementation Phases

### Phase 1: Setup DB models (Conversation, Message) and migrations
- Create Conversation and Message SQLModel entities in existing backend
- Implement database migration scripts for new tables
- Set up indexes for efficient querying with user_id isolation
- Implement conversation and message services in existing backend structure

### Phase 2: Implement MCP tools and server (integrated approach)
- Implement 5 task operation tools within existing backend:
  - add_task: Create a new task with user_id, title (required), description (optional)
  - list_tasks: Retrieve tasks with optional status filter (all, pending, completed)
  - complete_task: Mark a task as complete using user_id and task_id
  - delete_task: Remove a task using user_id and task_id
  - update_task: Modify task title or description using user_id, task_id, and optional new values
- Ensure all tools enforce user isolation via user_id validation
- Connect tools to existing database for persistence

### Phase 3: Configure OpenRouter + Agent logic
- Configure AsyncOpenAI client for OpenRouter with deepseek/deepseek-r1-0528:free model
- Implement OpenAI Agent with MCP tool integration
- Define agent behavior for natural language processing (task creation, listing, completion, deletion, updates)
- Implement confirmation and error handling patterns
- Integrate with existing authentication system

### Phase 4: Implement chat endpoint and conversation service
- Create FastAPI router for new `/api/{user_id}/chat` endpoint in existing backend
- Implement conversation state management with history persistence
- Integrate agent logic with endpoint using MCP tools
- Add JWT authentication and user validation using Better Auth
- Implement conversation history fetch/store from Neon DB

### Phase 5: Add Chat Widget and ChatKit UI in frontend
- Add Chat Widget as floating right-side button in existing layout
- Integrate ChatKit UI that opens when widget is clicked
- Implement secure connection to backend chat endpoint
- Add proper error handling and loading states
- Ensure responsive design across devices (320px to 1920px)

### Phase 6: Connect frontend to backend chat endpoint, test full flow
- Connect frontend ChatKit UI to backend `/api/{user_id}/chat` endpoint
- Test complete natural language command flow
- Validate user isolation and authentication
- Perform end-to-end testing of all 5 basic todo operations

## Quality Validation Strategy

### MCP Tools Unit Testing
- Test each MCP tool individually for proper functionality
- Validate user_id isolation with 403 error responses for unauthorized access
- Test parameter validation and error handling for each tool
- Verify proper database operations for each tool

### Chat Endpoint Integration Testing
- Test conversation history persistence and retrieval
- Validate JWT authentication and user_id extraction
- Verify conversation resumption after server restart
- Test stateless operation with proper state management

### Natural Language Command Testing
- Test all specified command patterns for correct tool invocation
- Validate confirmation responses for all successful operations
- Test error handling for invalid commands and non-existent tasks
- Verify proper user isolation across different user accounts

### OpenRouter Model Validation
- Test deepseek/deepseek-r1-0528:free model integration
- Validate response times and quality
- Monitor API usage and costs

### Frontend Integration Testing
- Test Chat Widget appearance and responsiveness across all screen sizes
- Validate seamless integration with existing UI components
- Verify proper error handling and loading states
- Confirm accessibility compliance (WCAG 2.1 AA)

## Trade-offs Analysis

### AI Framework Choice
- **Choice**: OpenAI Agents SDK via OpenRouter
- **Pros**: Cost-free, no OpenAI key required, wide model selection
- **Cons**: Limited models compared to direct OpenAI, potential rate limits

### MCP Tools Integration Approach
- **Choice**: Integrate MCP tools within existing backend (not standalone)
- **Pros**: Single codebase, easier maintenance, simpler deployment
- **Cons**: Tighter coupling between components, potential complexity in existing backend

### Stateless Design with DB Persistence
- **Choice**: Database persistence instead of in-memory sessions
- **Pros**: Scalability, conversation history, cross-device access
- **Cons**: Additional database load, complexity in state management

### Frontend Approach
- **Choice**: OpenAI ChatKit widget
- **Pros**: Easy integration, maintained UI, reduced development time
- **Cons**: Less customization, dependency on OpenAI infrastructure

## Risk Assessment

### High Risks
- **OpenRouter Availability**: Service stability and model availability
- **MCP Integration Complexity**: Challenges in integrating MCP tools within existing backend
- **User Isolation**: Security vulnerabilities in user data access
- **Frontend Integration**: Potential conflicts with existing UI components

### Mitigation Strategies
- Implement fallback mechanisms for API failures
- Thorough testing of MCP tool security within existing backend
- Comprehensive authentication validation
- Careful integration testing with existing frontend components