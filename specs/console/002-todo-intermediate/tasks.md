# Tasks: The Evolution of Todo – Intermediate Level

**Input**: Design documents from `/specs/002-todo-intermediate/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Unit tests for filtering, sorting, and metadata logic are included as requested in the implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure updates

- [x] T001 Update `Task` data model with priority, tags, and due_date in `src/models.py`
- [x] T002 Update `TodoService` `add_task` and `update_task` signatures to support new metadata in `src/todo_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logic for organization (Priority, Tags, Due Dates)

- [x] T003 Implement priority mapping and default values in `src/todo_service.py`
- [x] T004 Implement tag validation (max 3) and normalization in `src/todo_service.py`
- [x] T005 Implement date validation logic for `YYYY-MM-DD` in `src/todo_service.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task Organization (Priority & Tags) (Priority: P1)

**Goal**: Allow users to assign and view priorities and labels

### Implementation for User Story 1

- [x] T006 [P] [US1] Update `run_add_task` CLI flow to capture priority and tags in `src/cli.py`
- [x] T007 [P] [US1] Implement field-specific sub-menu for metadata updates in `src/cli.py`
- [x] T008 [US1] Update task display formatting to include priority and tags in `src/cli.py`

**Checkpoint**: User Story 1 is functional - tasks can be organized and viewed with metadata

---

## Phase 4: User Story 2 - Search Tasks (Priority: P1)

**Goal**: Quickly find tasks by keyword

### Tests for User Story 2
- [x] T009 [P] [US2] Create unit test for case-insensitive keyword search in `tests/unit/test_search.py`

### Implementation for User Story 2

- [x] T010 [US2] Implement `search_tasks(keyword)` method in `src/todo_service.py`
- [x] T011 [US2] Create Search & Filter CLI sub-menu with keyword search option in `src/cli.py`

**Checkpoint**: User Story 2 is functional - tasks are searchable by keyword

---

## Phase 5: User Story 3 - Filter and Sort Tasks (Priority: P2)

**Goal**: Slice and dice task list by status, priority, or tag

### Tests for User Story 3
- [x] T012 [P] [US3] Create unit tests for status, priority, and tag filtering in `tests/unit/test_filters.py`
- [x] T013 [P] [US3] Create unit tests for priority and alphabetical sorting in `tests/unit/test_sorting.py`

### Implementation for User Story 3

- [x] T014 [US3] Implement `filter_tasks(status, priority, tag)` method in `src/todo_service.py`
- [x] T015 [US3] Implement `sort_tasks(criterion)` method in `src/todo_service.py`
- [x] T016 [US3] Integrate filter options into Search & Filter CLI sub-menu in `src/cli.py`
- [x] T017 [US3] Create Sorting CLI sub-menu with priority and alphabetical options in `src/cli.py`

**Checkpoint**: User Story 3 is functional - tasks can be filtered and sorted

---

## Phase 6: User Story 4 - Due Dates (Priority: P2)

**Goal**: Track deadlines and sort by urgency

### Implementation for User Story 4

- [x] T018 [US4] Update CLI to capture due_date during add/update with immediate re-prompt on invalid in `src/cli.py`
- [x] T019 [US4] Implement "Sort by Due Date" (Oldest First) logic in `src/todo_service.py`
- [x] T020 [US4] Add "Sort by Due Date" option to Sorting CLI sub-menu in `src/cli.py`

**Checkpoint**: User Story 4 is functional - tasks support deadlines and chronological sorting

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T021 [P] Ensure all Phase-I operations (Add, Delete, etc.) work with updated Task objects
- [x] T022 Update README.md with instructions for new organization features
- [x] T023 Run end-to-end traversal of all menus to verify usability
