---
id: 0013
title: auto-reschedule-weekly-fix
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.fix
labels: [auto-reschedule, weekly, recurrence, bug-fix]
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

Fix Auto Reschedule functionality that wasn't working properly for weekly tasks.

## Response snapshot

Successfully fixed the Auto Reschedule functionality, particularly addressing the weekly rescheduling logic issue:

## Changes Made:

1. **Fixed weekly rescheduling calculation** in `src/todo_service.py`:
   - Corrected the algorithm for calculating same weekday next week
   - The formula `(target_weekday - reference_date.weekday()) % 7` properly calculates days to advance
   - Added special handling for when the target weekday equals the reference weekday (adds 7 days for next week)
   - Now correctly reschedules weekly tasks to the same weekday in the next week

2. **Maintained existing functionality**:
   - Daily tasks still reschedule to today
   - Monthly tasks still reschedule to same day next month
   - Non-recurring tasks still reschedule to reference date
   - Only incomplete overdue tasks are rescheduled
   - Completed tasks remain untouched

## Key Features:
- Auto Reschedule now correctly handles all recurrence types
- Weekly tasks properly reschedule to same weekday next week
- All other recurrence types continue to work as expected
- Filtering for incomplete overdue tasks preserved
- All existing functionality maintained

## Outcome

- ✅ Impact: Auto Reschedule functionality now works correctly for all recurrence types
- 🧪 Tests: All tests pass, functionality verified with comprehensive testing
- 📁 Files: Updated todo_service.py with corrected weekly calculation
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Implementation properly addresses the specific bug while preserving all other functionality

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Bug fix implementation prompt
- Next experiment (smallest change to try): User validation of the corrected behavior
