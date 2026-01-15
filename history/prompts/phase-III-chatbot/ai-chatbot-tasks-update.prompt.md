---
id: PHR-004-ai-chatbot-tasks-update
title: "AI Chatbot Tasks Update"
stage: tasks
feature: "ai-chatbot"
created: 2026-01-14T18:30:00Z
status: completed
tags: [tasks, update, ai, chatbot, structure, ui]
---

# AI Chatbot Tasks Update

## Original Prompt

Update Tasks for Phase-III Todo AI Chatbot Integration

Update the existing tasks.md to include OpenRouter configuration, project structure updates, and all missing foundational tasks for Phase-III. Ensure the file reflects integration into the existing Phase-II app (right-side Chat Widget, new backend endpoint, new DB models, MCP tools, agent logic).

Add these new tasks (with IDs starting from T041):

T041: Create project structure updates section in tasks.md showing new frontend/backend files (ChatWidget.tsx, chat/page.tsx, chat.py, conversation.py, message.py, etc.)
T042: Implement OpenRouter configuration (AsyncOpenAI client, base_url, OPENROUTER_API_KEY from .env) in backend/src/services/openrouter_client.py
T043: Set up domain allowlist and NEXT_PUBLIC_OPENAI_DOMAIN_KEY configuration for hosted ChatKit in frontend
T044: Add Chat Widget (floating right-side button) in frontend/app/layout.tsx or components
T045: Implement Chat Interface (ChatKit UI) in frontend/app/chat/page.tsx or components/ChatInterface.tsx
T046: Update frontend/lib/api.ts to include POST /api/{user_id}/chat calls

Prioritize:
T041-T042 (structure and OpenRouter) first
T043-T046 (UI integration) after backend foundation

Dependencies: After updated spec/plan and MCP tools

Output: Updated tasks.md with new section for structure, added tasks (T041+), priorities, dependencies, and acceptance tests where applicable. Keep existing tasks intact. Generate inside /specs/phase-III-chatbot/tasks.md.

## Response Summary

Successfully updated the tasks.md file with new tasks for Phase-III Todo AI Chatbot integration:

Phase 6: Project Structure Updates
- T041: Created project structure updates section showing new frontend/backend files
- T042: Implemented OpenRouter configuration task (marked as parallelizable [P])
- T043: Set up domain allowlist and NEXT_PUBLIC_OPENAI_DOMAIN_KEY configuration

Phase 7: UI Integration Tasks
- T044: Add Chat Widget (floating right-side button)
- T045: Implement Chat Interface (ChatKit UI)
- T046: Update frontend API to include chat endpoint calls

Phase 8: Polish & Cross-Cutting Concerns (tasks T032-T040 moved to this phase)

The tasks maintain the proper checklist format with checkboxes, sequential IDs, parallel markers where appropriate, and clear file paths. The updated structure ensures that foundational tasks (structure and OpenRouter) come first, followed by UI integration tasks that depend on the backend foundation.

## Key Changes

1. Reorganized phases to accommodate new structural tasks
2. Added tasks T041-T046 with proper formatting
3. Maintained all existing tasks (T001-T040)
4. Preserved user story labeling for relevant tasks
5. Ensured proper task dependencies and priorities

## Status

Tasks update completed successfully. The tasks.md file now includes all requested tasks with proper organization and structure.