---
id: "0003"
title: "clarify-intermediate-todo"
stage: "spec"
date: "2025-12-31"
surface: "claude-code"
model: "claude-sonnet-4-5-20250929"
feature: "002-todo-intermediate"
branch: "002-todo-intermediate"
user: "standard"
command: "/sp.clarify"
labels: ["clarification", "spec", "intermediate"]
links:
  spec: "specs/002-todo-intermediate/spec.md"
  ticket: "n/a"
  adr: "n/a"
  pr: "n/a"
files:
  - path: "specs/002-todo-intermediate/spec.md"
    status: "modified"
tests:
  - name: "spec-validation"
    status: "pass"
---

## Prompt

/sp.clarify

## Response snapshot

Resolved 5 critical ambiguities regarding the Intermediate Level implementation:
1. **Edit behavior**: Opted for a field-specific sub-menu for metadata updates.
2. **Sort Order**: Defaulted to "Oldest First" (chronological) for due dates.
3. **Tag Limit**: Restricted to a maximum of 3 tags per task.
4. **Invalid Input**: Implemented immediate re-prompt for invalid date strings.
5. **Case Sensitivity**: Standardized on case-insensitive search and filtering.

## Outcome

- ✅ Impact: High. Provides concrete UI/UX rules that prevent rework during the implementation phase.
- 🧪 Tests: n/a
- 📁 Files: specs/002-todo-intermediate/spec.md
- 🔁 Next prompts: /sp.plan, /sp.tasks
- 🧠 Reflection: Defining a field-specific sub-menu for updates is much better for UX than re-prompting for every field, especially as the task model grows.
