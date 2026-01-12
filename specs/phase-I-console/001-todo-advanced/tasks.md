# Tasks: Advanced Level - Intelligent Task Management

**Input**: Design documents from `/specs/001-todo-advanced/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Unit tests for recurrence intervals, cloning logic, and alert triggers are included as requested in the implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure updates

- [x] T001 Update `Task` data model with `due_time`, `recurrence`, and `root_id` in `src/models.py`
- [x] T002 Update `TodoService` `add_task` and `update_task` to support recurrence and time in `src/todo_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logic for recurrence engine and time validation

- [x] T003 Implement 24-hour time validation logic (HH:MM) in `src/todo_service.py`
- [x] T004 [P] Implement `Daily` and `Weekly` date increment logic in `src/todo_service.py`
- [x] T005 [P] Implement `Monthly` date increment logic with end-of-month handling in `src/todo_service.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1) 🎯 Intelligent MVP

**Goal**: Automate routine task maintenance via cloning

### Tests for User Story 1
- [x] T006 [P] [US1] Create unit tests for task cloning and date increments in `tests/unit/test_recurrence.py`

### Implementation for User Story 1
- [x] T007 [US1] Implement `_clone_recurring_task(task_id)` internal method in `src/todo_service.py`
- [x] T008 [US1] Update `toggle_complete` logic to trigger `_clone_recurring_task` for recurring items in `src/todo_service.py`
- [x] T009 [US1] Update `run_add_task` CLI flow to capture recurrence interval in `src/cli.py`
- [x] T010 [US1] Ensure `delete_task` logic correctly handles recurring task series in `src/todo_service.py`

**Checkpoint**: User Story 1 is functional - tasks automatically repeat upon completion

---

## Phase 4: User Story 2 - Due Time & Notifications (Priority: P1)

**Goal**: Precise scheduling and proactive console alerts

### Tests for User Story 2
- [x] T011 [P] [US2] Create unit test for deadline check logic in `tests/unit/test_alerts.py`

### Implementation for User Story 2
- [x] T012 [US2] Implement `get_upcoming_alerts()` method in `src/todo_service.py`
- [x] T013 [US2] Create a background `NotificationThread` class in `src/cli.py`
- [x] T014 [US2] Update menu display logic to show active alert section in `src/cli.py`
- [x] T015 [US2] Integrate `due_time` input and formatting into CLI task view in `src/cli.py`

**Checkpoint**: User Story 2 is functional - imminent deadlines trigger console alerts

---

## Phase 5: User Story 3 - Intelligent Rescheduling (Priority: P2)

**Goal**: Recover from backlogs via batch rescheduling

### Implementation for User Story 3
- [x] T016 [US3] Implement `reschedule_overdue_tasks(new_date)` in `src/todo_service.py`
- [x] T017 [US3] Create "Advanced / Intelligence" CLI sub-menu in `src/cli.py`
- [x] T018 [US3] Add "Batch Reschedule Overdue to Today" option to sub-menu in `src/cli.py`

**Checkpoint**: User Story 3 is functional - backlog recovery is automated

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T019 [P] Verify metadata (priority, tags) persistence across task clones in `src/todo_service.py`
- [x] T020 [P] Implement terminal bell or visual indicator for high-priority imminent alerts in `src/cli.py`
- [x] T021 Update README.md with examples of 3 routine recurring tasks
- [x] T022 Final traversal of all menus to verify thread safety and shutdown procedure

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup & Foundational (Phase 1-2)**: MUST complete before any functional stories.
- **User Story 1 (P1)**: Prerequisite for automated management.
- **User Story 2 (P1)**: Can be implemented in parallel with US1 at the service level, but UI depends on the metadata updates.
- **User Story 3 (P2)**: Depends on US2's overdue detection logic.

### Parallel Opportunities

- Unit tests (T006, T011) can be written simultaneously.
- Date increment logic (T004, T005) can be developed independently.
- CLI formatting (T015) and Alert display (T014) can be worked on concurrently.

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup + Foundational date logic.
2. Complete Recurrence engine (cloning upon completion).
3. **STOP and VALIDATE**: Verify a "Daily" task creates tomorrow's instance correctly.

### Incremental Delivery

1. Integrate Due Times and simple CLI alerts (US2).
2. Implement Batch Rescheduling (US3).
3. Final hardening and documentation.
