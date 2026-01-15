---
id: PHR-001-ai-chatbot-spec
title: "AI Chatbot Specification Creation"
stage: spec
feature: "ai-chatbot"
created: 2026-01-14T14:31:00Z
status: completed
tags: [specification, ai, chatbot, todo, natural-language]
---

# AI Chatbot Specification Creation

## Original Prompt

Phase-III Todo AI Chatbot - Core Conversational Interface & Integration

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

Generate the main spec.md file for Phase-III inside /specs/phase-III-chatbot/spec.md with sections: Objective, Requirements, Architecture, Database Models, Chat API Endpoint, MCP Tools Specification, Agent Behavior, Conversation Flow, Natural Language Commands, Deliverables.

## Response Summary

Successfully created the main specification file for the Phase-III Todo AI Chatbot at `specs/phase-III-chatbot/spec.md`. The specification includes all required sections:
- User Scenarios & Testing with prioritized user stories
- Functional Requirements (FR-001 through FR-014)
- Key Entities definition
- Success Criteria with measurable outcomes (SC-001 through SC-008)
- Objective
- Architecture
- Database Models
- Chat API Endpoint specification
- MCP Tools Specification
- Agent Behavior guidelines
- Conversation Flow
- Natural Language Commands examples
- Deliverables

Also created a validation checklist at `specs/phase-III-chatbot/checklists/requirements.md` to ensure specification quality.

## Key Decisions Made

1. Used "ai-chatbot" as the short name for the feature
2. Assigned number 1 as no existing branches/directories were found
3. Created comprehensive functional requirements covering all aspects of the feature
4. Defined measurable success criteria that are technology-agnostic
5. Included proper user isolation and security considerations
6. Ensured compatibility with existing Phase-II infrastructure

## Status

Completed successfully. The specification is ready for the next phase (planning).