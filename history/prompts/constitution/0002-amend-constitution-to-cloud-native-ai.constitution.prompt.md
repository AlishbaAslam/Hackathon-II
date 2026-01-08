---
id: 0002
title: amend-constitution-to-cloud-native-ai
stage: constitution
date: 2026-01-04
surface: command
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Code
command: /sp.constitution
labels: [constitution, sdd, cloud-native, ai]
links:
  spec:
  ticket:
  adr:
  pr:
files:
- path: .specify/memory/constitution.md
  action: updated
  description: "Updated constitution to reflect cloud-native AI evolution"
- path: .specify/templates/plan-template.md
  action: updated
  description: "Added constitution principles check"
- path: .specify/templates/spec-template.md
  action: updated
  description: "Added constitution alignment section"
- path: .specify/templates/tasks-template.md
  action: updated
  description: "Added constitution compliance task"
tests:
- type: manual
  description: "Verified constitution principles alignment"
  result: pass
---

## Prompt

```
Project: Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI
Core principles:
Spec-Driven Development (SDD) mandatory for all implementations
No manual code writing – all code generated via Claude Code after refining specs
Adherence to Agentic Dev Stack: AGENTS.md + Spec-Kit Plus + Claude Code
Progressive evolution from CLI to distributed cloud-native AI system
Use of AI agents for intelligent features and deployments
Security and user isolation through authentication and JWT
Stateless architecture for scalability and resilience
Event-driven design for advanced features like reminders and recurring tasks
Key standards:
All features must have a dedicated Markdown Constitution and Spec in /specs folder
Reference specs using @specs/path/to/file.md in Claude Code prompts
Repository structure: Monorepo with /frontend, /backend, /specs, CLAUDE.md files at root and subfolders
Technology stack compliance: As specified per phase (e.g., Python for Phase I, Next.js + FastAPI for Phase II)
MCP tools for AI interactions: Stateless, database-persisted, with defined schemas
Deployment: Local Minikube for Phase IV, Cloud (DigitalOcean DOKS) for Phase V
Bonus features: Reusable intelligence, cloud-native blueprints, multi-language (Urdu), voice commands
Documentation: README.md with setup, CLAUDE.md with guidelines, demo video ≤90 seconds
Constraints:
Complete phases sequentially (I to V), no skipping
No freestyle coding or architecture changes without spec updates
Use only specified tools (e.g., OpenAI ChatKit, Agents SDK, MCP SDK, Dapr, Kafka/Redpanda)
GitHub repo must be public with /specs history, /src code, migrations
Deployments: Vercel for frontend, Neon DB for persistence, Kubernetes for Phases IV-V
CI/CD via GitHub Actions for Phase V
No vendor lock-in – use Dapr for abstraction where applicable
Success criteria:
All Basic, Intermediate, and Advanced features implemented and demonstrable
Chatbot handles natural language for todo management with confirmations and error handling
Successful local (Minikube) and cloud (DOKS) deployments with monitoring/logging
Zero manual code – verifiable through spec iterations and Claude Code history
Passes judge review: Process, prompts, iterations, and working demo
Bonus points achieved for exceptional features
Total points: 1,000 base + up to 600 bonus
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read any command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.
```

## Response snapshot

The constitution was updated from version 1.1.0 to 2.0.0 to reflect the evolution from CLI to distributed cloud-native AI system. Key changes include:

- Added new core principles: Cloud Native Architecture, AI Agent Integration, Security & Authentication, Event-Driven Design
- Expanded project scope governance to include all 5 phases (I-V)
- Updated technical standards to reflect progression from Python CLI to Next.js + FastAPI
- Added deployment standards for Kubernetes and cloud environments
- Updated success criteria to include cloud-native and AI features
- Updated dependent templates to include constitution compliance checks

## Outcome

- ✅ Impact: Major constitution overhaul reflecting project evolution to cloud-native AI system
- 🧪 Tests: Manual verification of constitution alignment with project goals
- 📁 Files: Updated constitution.md and 3 template files to maintain consistency
- 🔁 Next prompts: Plan and implement next phase features based on updated constitution
- 🧠 Reflection: Constitution now properly reflects the full scope of the project's evolution from CLI to cloud-native AI system

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement Phase II features based on updated constitution
