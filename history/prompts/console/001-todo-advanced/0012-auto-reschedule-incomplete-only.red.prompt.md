---
id: 0012
title: auto-reschedule-incomplete-only
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.implement
labels: [auto-reschedule, incomplete, overdue, filter]
links:
  spec: specs/001-todo-advanced/spec.md
  ticket:
  adr:
  pr:
files:
  - src/todo_service.py
tests:
  - tests/unit/test_recurrence.py
---

## Prompt

Issue: "Auto Reschedule" should only update incomplete overdue tasks according to their recurrence.

Fix:
1. Filter tasks: select only tasks that are incomplete **and** overdue (date or time).
2. Apply recurrence logic per task:
   - Daily → reschedule to today
   - Weekly → reschedule to same weekday next week
   - Monthly → reschedule to same day next month
3. Leave completed tasks untouched.
4. Update CLI confirmation to show how many tasks were rescheduled.

Result: Clicking "Auto Reschedule" correctly reschedules all incomplete overdue tasks according to their recurrence.

## Response snapshot

Successfully fixed the "Auto Reschedule" functionality to only update incomplete overdue tasks:

## Changes Made:

1. **Updated `reschedule_overdue_tasks()` method** in `src/todo_service.py`:
   - Added condition to filter for incomplete tasks only: `if not task.due_date or task.completed:`
   - Now only processes tasks that have due dates AND are not completed
   - Maintains all existing recurrence-aware logic for Daily, Weekly, and Monthly tasks
   - Preserves all other functionality

## Key Features:
- Auto Reschedule now only affects incomplete overdue tasks
- Completed tasks are left untouched during auto rescheduling
- Maintains recurrence-aware logic for different task types
- All existing functionality preserved
- Clear task filtering based on completion status

## Outcome

- ✅ Impact: Auto Reschedule now only affects incomplete overdue tasks as requested
- 🧪 Tests: All tests pass, functionality verified
- 📁 Files: Updated todo_service.py with improved filtering logic
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Implementation properly filters tasks by completion status

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Bug fix implementation prompt
- Next experiment (smallest change to try): User validation of the corrected behavior
