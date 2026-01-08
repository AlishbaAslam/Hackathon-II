---
id: '001'
title: 'Create project constitution'
stage: 'constitution'
date: '2025-12-30'
surface: 'agent'
model: 'claude-sonnet-4-5-20250929'
feature: 'none'
branch: 'master'
user: 'Claude Code user'
command: '/sp.constitution'
labels: ["constitution","setup"]
links:
  spec: 'null'
  ticket: 'null'
  adr: 'null'
  pr: 'null'
files:
  - /mnt/d/Hackathons/todo-console-app/.specify/memory/constitution.md
tests:
  - 'null'
---

## Prompt

/sp.constitution
Project: The Evolution of Todo – Phase I (In-Memory Python Console App)

Core principles:
Spec-driven development (all code must originate from approved specifications)
Simplicity and clarity for beginner-to-intermediate Python developers
Correctness of business logic (task lifecycle must behave predictably)
Maintainability (clean, readable, modular Python code)
Deterministic behavior (no hidden state, no side effects beyond in-memory data)

Key standards:
All features must be defined in specifications before implementation
Each change must produce a new spec entry in the specs history folder
Python code must follow PEP 8 conventions
Functions and classes must have clear, single responsibilities
No external persistence (no files, no databases, memory-only storage)

Functional requirements:
Add Task – Create a task with unique ID, title, description, and default incomplete status
Delete Task – Remove a task using its unique ID
Update Task – Modify title and/or description of an existing task
View Task List – Display all tasks with ID, title, description, and completion status
Mark as Complete – Toggle task completion state (complete/incomplete)

Technical constraints:
Language: Python 3.13+
Environment: UV-managed virtual environment
Architecture: Console-based application only
Storage: In-memory data structures (e.g., list or dictionary)
No third-party runtime dependencies (standard library only)

Project structure requirements:
Root-level constitution file (this document)
specs/ or specs-history/ directory containing all spec evolution files
src/ directory containing all Python source code
README.md with setup and execution instructions
CLAUDE.md defining Claude Code usage rules and expectations

Code quality rules:
No hard-coded magic values without explanation
Meaningful variable, function, and class names
Graceful handling of invalid user input
No duplicate logic across functions
Clear separation between user input, business logic, and output formatting

Documentation standards:
README.md must include:
- Project overview
- Setup instructions using UV
- How to run the console app
- Example usage flow
CLAUDE.md must clearly define:
- How Claude Code should generate specs
- How implementations must follow specs strictly

Success criteria:
All five basic-level features work correctly via console interaction
Application runs without errors in a fresh UV environment
Specifications fully describe the implemented behavior
Code passes manual review for cleanliness and readability
Project structure exactly matches defined deliverables

## Response snapshot

Created the project constitution file at:
- `.specify/memory/constitution.md`

The constitution establishes:
- Five core principles (Spec-Driven Development, Simplicity and Clarity, Correctness of Business Logic, Maintainability, Deterministic Behavior)
- Five functional requirements (Add, Delete, Update, View, Mark Complete)
- Technical constraints (Python 3.13+, UV, console-only, in-memory storage)
- Code standards (PEP 8, separation of concerns, no magic values)
- Required project structure
- Documentation standards
- Success criteria

## Outcome

- ✅ Impact: Established foundational governance document for the todo console app project
- 🧪 Tests: 'null'
- 📁 Files: /mnt/d/Hackathons/todo-console-app/.specify/memory/constitution.md
- 🔁 Next prompts: Create feature specification with /sp.specify, Generate implementation plan with /sp.plan
- 🧠 Reflection: Constitution serves as the source of truth for all project decisions. All future specs, plans, and implementations must align with these principles.

## Evaluation notes (flywheel)

- Failure modes observed: 'null'
- Graders run and results (PASS/FAIL): 'null'
- Prompt variant (if applicable): 'null'
- Next experiment (smallest change to try): 'null'
