---
id: 0011
title: auto-reschedule-recurrence-aware
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.implement
labels: [auto-reschedule, recurrence, overdue, batch]
links:
  spec: specs/001-todo-advanced/spec.md
  ticket:
  adr:
  pr:
files:
  - src/todo_service.py
  - src/cli.py
tests:
  - tests/unit/test_recurrence.py
---

## Prompt

Goal: Implement one-click "Auto Reschedule" that respects task recurrence.

Requirements:
* Menu Option: Rename Option 1 → "Auto Reschedule".
* Behavior:
  - Daily tasks → reschedule to today
  - Weekly tasks → reschedule to same weekday next week
  - Monthly tasks → reschedule to same day next month
* Applies to all overdue tasks, regardless of completion.
* Preserve task metadata (priority, tags, description).
* Display number of tasks rescheduled and their new due dates/times.

Files:
* src/todo_service.py – update `reschedule_overdue_tasks()` to handle recurrence-aware logic
* src/cli.py – rename menu option and connect it to updated method

## Response snapshot

Successfully implemented the one-click "Auto Reschedule" feature that respects task recurrence:

## Changes Made:

1. **Updated `reschedule_overdue_tasks()` method** in `src/todo_service.py`:
   - Modified to handle recurrence-aware logic for different recurrence types
   - Daily tasks → reschedule to reference date (today)
   - Weekly tasks → reschedule to same weekday next week
   - Monthly tasks → reschedule to same day next month (with proper month-end handling)
   - Non-recurring tasks → reschedule to reference date
   - Applies to all overdue tasks regardless of completion status
   - Preserves all task metadata (priority, tags, description, time)

2. **Updated Intelligence menu** in `src/cli.py`:
   - Renamed Option 1 from "Batch Reschedule Overdue to Today" to "Auto Reschedule"
   - Updated functionality to use the enhanced reschedule method
   - Maintains Option 2 for specific date/time rescheduling

## Key Features:
- One-click auto rescheduling that respects task recurrence patterns
- Daily tasks rescheduled to today
- Weekly tasks rescheduled to same weekday next week
- Monthly tasks rescheduled to same day next month (with end-of-month handling)
- Applies to all overdue tasks regardless of completion status
- All metadata preserved during rescheduling
- Clear user feedback with rescheduled count
- Maintains backward compatibility with existing functionality

## Outcome

- ✅ Impact: Auto Reschedule feature implemented with recurrence-aware logic as requested
- 🧪 Tests: All tests pass, functionality verified
- 📁 Files: Updated todo_service.py and cli.py with new functionality
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Implementation provides intelligent rescheduling based on task patterns

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Feature implementation prompt
- Next experiment (smallest change to try): User validation of the new auto reschedule behavior
