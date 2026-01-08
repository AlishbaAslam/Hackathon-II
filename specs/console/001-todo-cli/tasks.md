# Tasks: Todo Console App - Phase I

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: Manual validation only (Phase I scope - no automated tests)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create src/ directory structure per implementation plan in src/
- [x] T002 Create src/__init__.py to make src a Python package
- [x] T003 Create pyproject.toml with UV configuration for Python 3.13+

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task dataclass in src/models.py with id, title, description, completed
- [x] T005 Create TodoService class in src/todo_service.py with in-memory task storage
- [x] T006 Implement TodoService._tasks list and _next_id counter in src/todo_service.py
- [x] T007 Implement TodoService.get_task() method for ID-based lookup in src/todo_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1) MVP

**Goal**: Users can create tasks with title, optional description, auto-generated ID, and incomplete status

**Independent Test**: Run app, select "Add Task", enter title "Buy groceries", verify task appears with ID 1 and incomplete status

### Implementation for User Story 1

- [x] T008 [US1] Implement TodoService.add_task() method in src/todo_service.py
- [x] T009 [US1] Add input validation for non-empty title in src/todo_service.py
- [x] T010 [US1] Create display_menu() function in src/cli.py
- [x] T011 [US1] Create get_menu_choice() function with 1-6 validation in src/cli.py
- [x] T012 [US1] Create get_task_input() function for title/description in src/cli.py
- [x] T013 [US1] Create run_add_task() function connecting CLI to TodoService in src/cli.py
- [x] T014 [US1] Integrate Add Task option (1) into main CLI menu in src/cli.py

**Checkpoint**: User Story 1 complete - users can add tasks with validation

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks with ID, title, description, and completion status

**Independent Test**: Add 2 tasks, select "View Tasks", verify both tasks display with correct information

### Implementation for User Story 2

- [x] T015 [US2] Implement TodoService.get_all_tasks() method in src/todo_service.py
- [x] T016 [US2] Create format_task_display() function in src/cli.py
- [x] T017 [US2] Create run_view_tasks() function in src/cli.py
- [x] T018 [US2] Handle empty list case with "No tasks" message in src/cli.py
- [x] T019 [US2] Integrate View Tasks option (2) into main CLI menu in src/cli.py

**Checkpoint**: User Story 2 complete - users can view all tasks

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P1)

**Goal**: Users can toggle task completion status (complete ↔ incomplete)

**Independent Test**: Add task, mark complete, verify "[X]", mark again, verify "[ ]"

### Implementation for User Story 3

- [x] T020 [US3] Implement TodoService.toggle_complete() method in src/todo_service.py
- [x] T021 [US3] Create get_task_id() function with validation in src/cli.py
- [x] T022 [US3] Create run_mark_complete() function in src/cli.py
- [x] T023 [US3] Integrate Mark Complete option (3) into main CLI menu in src/cli.py

**Checkpoint**: User Story 3 complete - users can toggle task completion

---

## Phase 6: User Story 4 - Update a Task (Priority: P2)

**Goal**: Users can modify task title and/or description by ID

**Independent Test**: Add task, update title, view tasks, verify new title displayed

### Implementation for User Story 4

- [x] T024 [US4] Implement TodoService.update_task() method in src/todo_service.py
- [x] T025 [US4] Create get_update_input() function for title/description in src/cli.py
- [x] T026 [US4] Create run_update_task() function in src/cli.py
- [x] T027 [US4] Integrate Update Task option (4) into main CLI menu in src/cli.py

**Checkpoint**: User Story 4 complete - users can update tasks

---

## Phase 7: User Story 5 - Delete a Task (Priority: P2)

**Goal**: Users can remove tasks by ID

**Independent Test**: Add 3 tasks, delete task 2, view tasks, verify tasks 1 and 3 remain

### Implementation for User Story 5

- [x] T028 [US5] Implement TodoService.delete_task() method in src/todo_service.py
- [x] T029 [US5] Create run_delete_task() function in src/cli.py
- [x] T030 [US5] Integrate Delete Task option (5) into main CLI menu in src/cli.py

**Checkpoint**: User Story 5 complete - users can delete tasks

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T031 Create main() entry point function in src/main.py
- [x] T032 Create run_cli() main loop in src/cli.py with while True
- [x] T033 Add Exit option (6) to main menu in src/cli.py
- [x] T034 Add error handling for non-numeric menu input in src/cli.py
- [x] T035 Add error handling for non-existent task IDs in src/todo_service.py
- [x] T036 Create README.md with setup and usage instructions
- [x] T037 Create CLAUDE.md with Claude Code usage rules
- [x] T038 Verify pyproject.toml is properly configured for uv run

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories (3-7) |
| Phase 3-7: User Stories | Phase 2 | Phase 8 (Polish) |
| Phase 8: Polish | All Stories | None |

### User Story Dependencies

| User Story | Priority | Dependencies |
|------------|----------|--------------|
| US1: Add Task | P1 | Phase 2 (Foundational) |
| US2: View Tasks | P1 | Phase 2, US1 (data) |
| US3: Mark Complete | P1 | Phase 2, US1 (data) |
| US4: Update Task | P2 | Phase 2, US1 (data) |
| US5: Delete Task | P2 | Phase 2, US1 (data) |

**Note**: All user stories depend on Phase 2 (foundational) and use data from US1, but are otherwise independent and can be tested on their own once US1 is complete.

### Within Each User Story

- Models → Services → CLI functions → Integration into menu
- Story complete before moving to next priority
- All validation handled by service layer

### Parallel Opportunities

- Phase 1 tasks T001-T003 can run in parallel
- Phase 2 tasks T004-T007 can run in parallel
- User Stories 2-5 can start in parallel after US1 (each is independent)
- Polish tasks T031-T038 can run in parallel (different files)

---

## Parallel Example: After Foundation

Once Phase 2 is complete, this team could work in parallel:

```
Developer A: User Story 1 (Add Task) → T008-T014
Developer B: User Story 2 (View Tasks) → T015-T019
Developer C: User Story 3 (Mark Complete) → T020-T023
Developer D: User Stories 4-5 (Update/Delete) → T024-T030
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test add task functionality
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → Deploy/Demo (MVP!)
3. Add User Story 2 → Test → Deploy/Demo
4. Add User Story 3 → Test → Deploy/Demo
5. Add User Stories 4-5 → Test → Deploy/Demo
6. Polish → Final deliverable

### After MVP

Once US1 is working, continue with US2, US3, then US4/US5 in priority order.

---

## Notes

- **[P]** tasks = different files, no dependencies
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Manual validation only - no automated tests in Phase I scope

---

## Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 3 | Project structure |
| Phase 2: Foundational | 4 | Task model, TodoService base |
| Phase 3: US1 (Add) | 7 | Add task with validation |
| Phase 4: US2 (View) | 5 | View all tasks |
| Phase 5: US3 (Complete) | 4 | Toggle completion |
| Phase 6: US4 (Update) | 4 | Update task fields |
| Phase 7: US5 (Delete) | 3 | Delete task |
| Phase 8: Polish | 8 | Entry point, docs, error handling |
| **Total** | **38** | |

**MVP Scope**: Phases 1-3 (12 tasks) - Basic add task functionality
