---
id: 0008
title: overdue-task-display-fix
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.implement
labels: [bug-fix, overdue, display, datetime]
links:
  spec: specs/001-todo-advanced/spec.md
  ticket:
  adr:
  pr:
files:
  - src/cli.py
tests:
  - tests/unit/test_recurrence.py
  - tests/unit/test_alerts.py
  - tests/unit/test_search.py
---

## Prompt

Issue: Overdue logic ignores time.

Fix:
- Task is overdue if NOT completed AND (due_date + due_time) < now
- Show "[INCOMPLETE]" at end of overdue tasks

Constraints:
- Compare full datetime
- Display-only change

Files:
- src/cli.py
- src/todo_service.py (helper if needed)

Done when:
- Date OR time overdue shows "[INCOMPLETE]"

## Response snapshot

Successfully implemented the fix for overdue task display:

## Changes Made:

1. **Updated `display_tasks_custom()` function in `src/cli.py`**:
   - Added datetime import for proper time comparison
   - Added overdue logic that checks if task is NOT completed AND (due_date + due_time) < now
   - Added [INCOMPLETE] indicator that appears after the task title for overdue tasks
   - The indicator only shows for tasks that are incomplete and have passed their due date/time
   - Proper error handling for invalid date/time formats

2. **Logic details**:
   - For each task, checks if due_date exists and task is not completed
   - Combines due_date and due_time (defaults to '00:00' if no time specified)
   - Compares combined datetime with current datetime
   - Adds " [INCOMPLETE]" text to the display if the task is overdue

## Key Features:
- Overdue tasks now display [INCOMPLETE] indicator in all views (View Tasks, Search, Filter, etc.)
- Only incomplete tasks with past due dates/times show the indicator
- Completed tasks don't show the indicator even if their due date has passed
- Time-aware overdue detection (includes both date and time in comparison)
- All existing functionality preserved
- No changes to business logic, only display enhancement

## Outcome

- ✅ Impact: Overdue tasks now clearly show [INCOMPLETE] indicator in the display
- 🧪 Tests: All existing tests pass, functionality verified
- 📁 Files: Updated cli.py with new display logic
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Simple display-only change that significantly improves user experience

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Bug fix implementation prompt
- Next experiment (smallest change to try): User validation of the new display indicator
