---
id: 0010
title: batch-reschedule-user-command
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.implement
labels: [batch-reschedule, user-command, overdue, datetime]
links:
  spec: specs/001-todo-advanced/spec.md
  ticket:
  adr:
  pr:
files:
  - src/todo_service.py
  - src/cli.py
tests:
  - tests/unit/test_recurrence.py::test_batch_reschedule_overdue_functionality
---

## Prompt

Goal: Batch reschedule only on user command.

Requirements:
* Reschedule overdue tasks (complete/incomplete) only when "Batch Reschedule Overdue to Today" is selected.
* Update both date & time; retain metadata & recurrence.
* No auto-reschedule on becoming overdue.
* Show rescheduled count in CLI.

Files:
* src/todo_service.py – `batch_reschedule_overdue(new_datetime)`
* src/cli.py – Intelligence menu call

## Response snapshot

Successfully implemented the batch reschedule functionality that only runs on user command:

## Changes Made:

1. **Removed auto-rescheduling functionality** in `src/todo_service.py`:
   - Removed all calls to `_check_overdue_recurring_tasks()` from task access methods
   - Methods affected: `search_tasks()`, `filter_tasks()`, `sort_tasks()`, `get_all_tasks()`, `get_upcoming_alerts()`
   - Ensures no automatic rescheduling happens when tasks become overdue

2. **Added new `batch_reschedule_overdue(new_datetime)` method** in `src/todo_service.py`:
   - Accepts both date and time in format "YYYY-MM-DD HH:MM"
   - Reschedules only overdue tasks (due date/time < current time)
   - Updates both date and time fields
   - Preserves all other metadata (priority, tags, recurrence, etc.)
   - Returns count of rescheduled tasks

3. **Enhanced Intelligence menu** in `src/cli.py`:
   - Added option 2: "Batch Reschedule Overdue to Specific Date/Time"
   - Updated option 1: Uses new function with default time of 00:00
   - Added proper input validation for datetime format
   - Shows rescheduled count to user

## Key Features:
- Batch rescheduling only happens when user explicitly selects it
- Both date and time are updated for overdue tasks
- All metadata preserved during rescheduling
- Proper validation and error handling
- Clear user feedback with rescheduled count
- No automatic rescheduling when tasks become overdue

## Outcome

- ✅ Impact: Batch rescheduling now only happens on user command as requested
- 🧪 Tests: All tests pass, including new test for batch reschedule functionality
- 📁 Files: Updated todo_service.py and cli.py with new functionality
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Implementation follows the principle of explicit user control over rescheduling

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Feature implementation prompt
- Next experiment (smallest change to try): User validation of the new batch reschedule workflow
