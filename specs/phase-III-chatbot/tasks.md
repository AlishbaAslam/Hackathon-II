# Implementation Tasks: Phase-III Todo AI Chatbot

**Feature**: Phase-III Todo AI Chatbot - Planning for Integration into Existing Phase-II App
**Spec Reference**: [spec.md](./spec.md)
**Plan Reference**: [plan.md](./plan.md)
**Created**: 2026-01-14

## Dependencies

- Phase 4 (chat endpoint) depends on Phase 1 (DB models) and Phase 2 (MCP tools) foundational components
- Phase 5 (frontend integration) depends on Phase 4 (backend endpoint) components
- Phase 6 (full flow testing) depends on all previous phases

## Parallel Execution Opportunities

- Database model creation (Conversation and Message) can run in parallel with MCP tools implementation
- Frontend components (ChatWidget and ChatInterface) can be developed in parallel with backend endpoint
- Individual MCP tools can be implemented in parallel after the infrastructure is set up
- OpenRouter configuration can run in parallel with MCP tools development

## Implementation Strategy

**MVP Scope**: Complete backend implementation (Phases 1-4) with basic frontend integration (Phase 5) and core functionality testing (Phase 6)
**Incremental Delivery**: Each phase builds upon the previous one, with each being independently testable

## Phase 1: Setup DB models (Conversation, Message) and migrations

- [ ] T001 Create Conversation SQLModel in backend/src/models/conversation.py following data-model.md
- [ ] T002 Create Message SQLModel in backend/src/models/message.py following data-model.md
- [ ] T003 Implement database migration for Conversation and Message tables
- [ ] T004 Set up indexes for efficient querying with user_id isolation in database
- [ ] T005 Implement conversation and message services in existing backend structure

## Phase 2: Implement MCP tools and server (integrated approach)

- [ ] T006 Implement add_task tool within existing backend in backend/src/mcp_tools/task_tools.py with user_id validation
- [ ] T007 Implement list_tasks tool within existing backend in backend/src/mcp_tools/task_tools.py with status filtering
- [ ] T008 Implement complete_task tool within existing backend in backend/src/mcp_tools/task_tools.py with user validation
- [ ] T009 Implement delete_task tool within existing backend in backend/src/mcp_tools/task_tools.py with user validation
- [ ] T010 Implement update_task tool within existing backend in backend/src/mcp_tools/task_tools.py with user validation
- [ ] T011 Ensure all tools enforce user isolation via user_id validation from JWT
- [ ] T012 Connect tools to existing database for persistence
- [ ] T013 Test tool functionality independently

## Phase 3: Configure OpenRouter + Agent logic

**Goal**: Configure AsyncOpenAI client for OpenRouter and implement OpenAI Agent with MCP tool integration

- [ ] T014 [P] [Phase 3] Configure AsyncOpenAI client for OpenRouter with deepseek/deepseek-r1-0528:free model in backend/src/services/openrouter_client.py
- [ ] T015 [P] [Phase 3] Implement OpenAI Agent with MCP tool integration in backend/src/services/agent_service.py
- [ ] T016 [P] [Phase 3] Define agent behavior for natural language processing in backend/src/services/agent_service.py
- [ ] T017 [P] [Phase 3] Implement confirmation and error handling patterns in agent behavior
- [ ] T018 [P] [Phase 3] Integrate with existing authentication system using Better Auth JWT

## Phase 4: Implement chat endpoint and conversation service

**Goal**: Create FastAPI router for /api/{user_id}/chat endpoint and implement conversation state management

- [ ] T019 [P] [Phase 4] Create FastAPI router for new /api/{user_id}/chat endpoint in backend/src/routers/chat.py
- [ ] T020 [P] [Phase 4] Implement conversation state management with history persistence in backend/src/services/conversation_service.py
- [ ] T021 [P] [Phase 4] Integrate agent logic with endpoint using MCP tools
- [ ] T022 [P] [Phase 4] Add JWT authentication and user validation using Better Auth in backend/src/routers/chat.py
- [ ] T023 [P] [Phase 4] Implement conversation history fetch/store from Neon DB in backend/src/services/conversation_service.py

## Phase 5: Add Chat Widget and ChatKit UI in frontend

**Goal**: Add Chat Widget as floating right-side button in existing layout and integrate ChatKit UI

- [ ] T024 [P] [Phase 5] Implement basic ChatWidget component as floating right-side button in frontend/components/chat/ChatWidget.tsx
- [ ] T025 [P] [Phase 5] Integrate ChatKit UI that opens when widget is clicked in frontend/components/chat/ChatInterface.tsx
- [ ] T026 [P] [Phase 5] Implement secure connection to backend chat endpoint in frontend/lib/api.ts and frontend/hooks/useChat.ts
- [ ] T027 [P] [Phase 5] Add proper error handling and loading states in frontend components
- [ ] T028 [P] [Phase 5] Ensure responsive design across devices (320px to 1920px) in frontend/components/chat/

## Phase 6: Connect frontend to backend chat endpoint, test full flow

**Goal**: Connect frontend ChatKit UI to backend /api/{user_id}/chat endpoint and perform comprehensive testing

- [ ] T029 [P] [Phase 6] Connect frontend ChatKit UI to backend /api/{user_id}/chat endpoint
- [ ] T030 [P] [Phase 6] Test complete natural language command flow for all 5 basic todo operations
- [ ] T031 [P] [Phase 6] Validate user isolation and authentication
- [ ] T032 [P] [Phase 6] Perform end-to-end testing of all natural language commands
- [ ] T033 [P] [Phase 6] Test conversation persistence across server restarts
- [ ] T034 [P] [Phase 6] Validate history restoration functionality

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T035 [P] Implement comprehensive logging for debugging and monitoring
- [ ] T036 [P] Add proper error handling and validation across all components
- [ ] T037 [P] Implement security measures to enforce user isolation in all operations
- [ ] T038 [P] Conduct security testing to verify user data isolation and 403 error responses
- [ ] T039 [P] Update README with Phase-III setup instructions from quickstart.md
- [ ] T040 [P] Set up domain allowlist and NEXT_PUBLIC_OPENAI_DOMAIN_KEY configuration for hosted ChatKit in frontend
- [ ] T041 [P] Perform end-to-end testing of all user stories
- [ ] T042 [P] Optimize database queries and add proper indexing as specified in data-model.md
- [ ] T043 [P] Conduct performance testing to ensure response times under 5 seconds (SC-006)