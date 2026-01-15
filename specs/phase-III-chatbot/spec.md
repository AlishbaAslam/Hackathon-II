# Feature Specification: Phase-III Todo AI Chatbot - Core Conversational Interface & Integration

**Feature Branch**: `1-ai-chatbot`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "Phase-III Todo AI Chatbot - Core Conversational Interface & Integration

Target: Add an AI-powered chatbot widget to the existing Phase-II full-stack Todo app, allowing users to manage tasks via natural language (add, list, update, complete, delete).

Focus: Right-side Chat Widget (click to open chat interface) → stateless chat endpoint → OpenAI Agents SDK (via OpenRouter) → MCP tools → Neon DB persistence. All specs must be created/updated inside the /specs/phase-III-chatbot/ folder.

Success criteria:
- Chat widget appears on right side of existing app (non-intrusive, responsive)
- Clicking widget opens chat interface (ChatKit UI)
- Natural language commands fully work for all 5 basic todo features
- Stateless server: conversation state stored in DB (Conversations + Messages tables)
- MCP server exposes 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) with user_id isolation
- Agent confirms actions (e.g., "Added task: Buy groceries") & handles errors gracefully
- OpenRouter used (no OpenAI key) with model like deepseek/deepseek-r1-0528:free
- Better Auth JWT used for user isolation on chat endpoint
- Domain allowlist & NEXT_PUBLIC_OPENAI_DOMAIN_KEY configured for hosted ChatKit

Constraints:
- Build on top of existing Phase-II code (frontend, backend, DB, auth) – no full rewrite
- No manual coding – all generation via Claude Code
- Use OpenRouter for all model calls (AsyncOpenAI client)
- Timeline: Core flow complete before advanced features
- Use Context7 MCP for all spec/doc access/updates
- All specification files (spec.md, overview.md, etc.) must be placed inside the /specs/phase-III-chatbot/ folder

Not implementing:
- Advanced features (recurring tasks, reminders, voice)
- Multi-language support
- Full new UI redesign (only add chat widget/interface)

Deliverables:
- Updated frontend (Chat Widget + ChatKit integration)
- New backend endpoint (/api/{user_id}/chat)
- MCP tools implementation
- New DB models (Conversation, Message)
- spec.md, plan.md, tasks.md inside /specs/phase-III-chatbot/
- README updates for Phase-III setup

Generate the main spec.md file for Phase-III inside /specs/phase-III-chatbot/spec.md with sections: Objective, Requirements, Architecture, Database Models, Chat API Endpoint, MCP Tools Specification, Agent Behavior, Conversation Flow, Natural Language Commands, Deliverables."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

As a user, I want to manage my tasks using natural language commands so that I can interact with my todo list more naturally without navigating through menus.

**Why this priority**: This is the core value proposition of the feature - enabling users to interact with their tasks conversationally, which significantly improves the user experience and accessibility.

**Independent Test**: Can be fully tested by engaging with the chatbot using natural language commands and verifying that all 5 basic todo operations (add, list, update, complete, delete) work correctly.

**Acceptance Scenarios**:

1. **Given** user is on the app page with the chat widget visible, **When** user clicks the chat widget and types "Add a task to buy groceries", **Then** the task "buy groceries" is created and confirmed back to the user
2. **Given** user has existing tasks in their list, **When** user asks "Show me all my tasks", **Then** the chatbot lists all tasks with their current status
3. **Given** user has a pending task, **When** user says "Mark task 3 as complete", **Then** the specified task is marked as complete and the user is notified of the change

---

### User Story 2 - Persistent Conversation Experience (Priority: P2)

As a user, I want my conversation with the chatbot to persist across sessions so that I can continue my task management conversations seamlessly.

**Why this priority**: Ensures continuity of user experience and allows for complex multi-turn conversations about task management.

**Independent Test**: Can be fully tested by starting a conversation, closing the browser, returning later, and continuing the conversation where it left off.

**Acceptance Scenarios**:

1. **Given** user has an ongoing conversation with the chatbot, **When** user closes the browser and returns later, **Then** user can see their conversation history and continue the discussion
2. **Given** user is logged in, **When** user interacts with the chatbot, **Then** all conversation data is securely stored and isolated to that user's account

---

### User Story 3 - Intelligent Task Actions Confirmation (Priority: P3)

As a user, I want the chatbot to confirm my actions and handle errors gracefully so that I can trust the system and recover from mistakes easily.

**Why this priority**: Critical for user confidence and error prevention, ensuring that unintended actions don't negatively impact the user's task list.

**Independent Test**: Can be fully tested by performing various task operations and verifying that the bot confirms successful actions and provides helpful error messages when issues occur.

**Acceptance Scenarios**:

1. **Given** user issues a task modification command, **When** the action is processed successfully, **Then** the chatbot confirms the action with specific details (e.g., "Added task: Buy groceries")
2. **Given** user provides an invalid command or references a non-existent task, **When** the error occurs, **Then** the chatbot provides a helpful error message and suggests alternatives

---

### Edge Cases

- What happens when a user tries to access another user's tasks through the chatbot? (User isolation must be enforced)
- How does the system handle malformed natural language that doesn't map to any known task operations?
- What occurs when the database is temporarily unavailable during a conversation?
- How does the system handle extremely long conversations that might exceed memory/database limits?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a right-side chat widget that appears non-intrusively on the existing app interface
- **FR-002**: System MUST allow users to open and interact with the chat interface using ChatKit UI
- **FR-003**: System MUST interpret natural language commands for all 5 basic todo operations (add, list, update, complete, delete)
- **FR-004**: System MUST persist conversation state in the database using Conversation and Message entities
- **FR-005**: System MUST expose 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) for the AI agent
- **FR-006**: System MUST isolate user data using Better Auth JWT tokens to prevent cross-user access
- **FR-007**: System MUST confirm all user actions with friendly responses (e.g., "Added task: Buy groceries")
- **FR-008**: System MUST handle errors gracefully with appropriate user feedback
- **FR-009**: System MUST use OpenRouter for all AI model calls without requiring OpenAI keys
- **FR-010**: System MUST ensure the chat widget is responsive across all device sizes
- **FR-011**: System MUST integrate with existing Phase-II authentication system using Better Auth
- **FR-012**: System MUST store conversation history in Neon DB with proper user_id isolation
- **FR-013**: System MUST provide a stateless backend endpoint at /api/{user_id}/chat
- **FR-014**: System MUST configure domain allowlist and NEXT_PUBLIC_OPENAI_DOMAIN_KEY for hosted ChatKit

### Key Entities

- **Conversation**: Represents a chat session for a user, containing metadata like creation time and user association
- **Message**: Represents individual messages within a conversation, including sender role (user/assistant), content, and timestamp
- **Task**: Represents todo items with title, description, completion status, and user ownership
- **User**: Represents authenticated users with JWT-based authentication and authorization

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chat widget appears on right side of existing app interface and is responsive across all screen sizes (320px to 1920px)
- **SC-002**: Natural language commands successfully process all 5 basic todo operations with 95% accuracy rate
- **SC-003**: Conversation state persists reliably in database with 99.9% availability
- **SC-004**: Users can successfully manage tasks via chat interface within 3 minutes of first interaction
- **SC-005**: System handles user isolation properly with 0 cross-user data access incidents
- **SC-006**: AI agent responds to user commands within 5 seconds average response time
- **SC-007**: All 5 MCP tools function correctly with proper error handling and user feedback
- **SC-008**: Chat interface integrates seamlessly with existing Phase-II authentication system

### Constitution Alignment

- **SDD Compliance**: Feature originates from approved specification
- **Progressive Evolution**: Feature builds upon existing Phase-II infrastructure without requiring rewrite
- **Cloud Native**: Stateless architecture with externalized state in Neon DB
- **AI Integration**: Natural language processing and AI-powered task management
- **Security**: Proper authentication/authorization with JWT and user isolation
- **Event-Driven**: Asynchronous processing of chat interactions and task operations

## Objective

The objective of this feature is to enhance the existing Phase-II Todo application by adding an AI-powered chatbot widget that allows users to manage their tasks through natural language commands. This adds a conversational interface layer that provides an alternative, more intuitive way to interact with the task management system.

## Architecture

The architecture follows a layered approach:
- Frontend: Right-side chat widget using ChatKit UI that communicates with backend
- Backend: Stateless FastAPI endpoint that handles chat requests and manages conversation state
- AI Layer: OpenAI Agents SDK (via OpenRouter) that interprets natural language and calls MCP tools
- MCP Layer: MCP tools server that exposes task operations as callable functions
- Data Layer: Neon PostgreSQL database storing conversations, messages, and tasks with user isolation
- Authentication: Better Auth JWT system for user identification and authorization

## Database Models

- **Conversation**: Stores conversation metadata including user_id, id, created_at, updated_at
- **Message**: Stores individual messages with user_id, id, conversation_id, role (user/assistant), content, created_at
- **Task**: Stores todo items with user_id, id, title, description, completed status, created_at, updated_at

## Chat API Endpoint

- **Endpoint**: POST /api/{user_id}/chat
- **Purpose**: Handle natural language messages and return AI-generated responses
- **Request Parameters**: conversation_id (optional), message (required)
- **Response**: conversation_id, response, tool_calls array
- **Authentication**: JWT token verification and user_id extraction from Better Auth

## MCP Tools Specification

The MCP server must expose the following tools:

- **add_task**: Creates a new task with user_id, title (required), description (optional)
- **list_tasks**: Retrieves tasks with optional status filter (all, pending, completed)
- **complete_task**: Marks a task as complete using user_id and task_id
- **delete_task**: Removes a task using user_id and task_id
- **update_task**: Modifies task title or description using user_id, task_id, and optional new values

## Agent Behavior

- **Task Creation**: When user mentions adding/creating/remembering something, use add_task
- **Task Listing**: When user asks to see/show/list tasks, use list_tasks with appropriate filter
- **Task Completion**: When user says done/complete/finished, use complete_task
- **Task Deletion**: When user says delete/remove/cancel, use delete_task
- **Task Update**: When user says change/update/rename, use update_task
- **Confirmation**: Always confirm actions with friendly response
- **Error Handling**: Gracefully handle task not found and other errors

## Conversation Flow

1. User sends message via chat interface
2. Backend fetches conversation history from database
3. Message array is built combining history with new message
4. User message is stored in database
5. AI agent runs with MCP tools access
6. Agent invokes appropriate MCP tool(s) based on natural language
7. Assistant response is stored in database
8. Response is returned to client
9. Server remains stateless (ready for next request)

## Natural Language Commands

The chatbot should understand and respond to commands like:
- "Add a task to buy groceries" → Calls add_task with title "Buy groceries"
- "Show me all my tasks" → Calls list_tasks with status "all"
- "What's pending?" → Calls list_tasks with status "pending"
- "Mark task 3 as complete" → Calls complete_task with task_id 3
- "Delete the meeting task" → Calls list_tasks first, then delete_task
- "Change task 1 to 'Call mom tonight'" → Calls update_task with new title
- "I need to remember to pay bills" → Calls add_task with title "Pay bills"
- "What have I completed?" → Calls list_tasks with status "completed"

## Deliverables

- Updated frontend with Chat Widget and ChatKit integration
- New backend endpoint at /api/{user_id}/chat
- MCP tools implementation with 5 task operations
- New database models for Conversation and Message
- spec.md, plan.md, tasks.md files in /specs/phase-III-chatbot/
- README updates for Phase-III setup instructions