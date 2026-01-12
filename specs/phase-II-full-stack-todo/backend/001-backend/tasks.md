---
description: "Task list for Phase-II FastAPI Backend with user-scoped CRUD operations"
---

# Tasks: Phase-II FastAPI Backend for Full-Stack Todo Web Application

**Input**: Design documents from `/specs/backend/001-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- Paths shown below follow the plan.md structure for the backend project

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure per plan.md with src/, tests/, config files
- [ ] T002 [P] Configure pyproject.toml with dependencies from research.md
- [ ] T003 Create .env.example template with all environment variables from research.md
- [ ] T004 Setup basic FastAPI application in backend/src/main.py with CORS configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Setup database schema and SQLModel configuration in backend/src/core/database.py
- [ ] T006 [P] Implement password hashing utilities in backend/src/core/security.py using bcrypt
- [ ] T007 [P] Implement JWT utilities in backend/src/core/security.py for token generation/verification
- [ ] T008 Create SQLModel User model in backend/src/models/user.py following data-model.md
- [ ] T009 Create SQLModel Task model in backend/src/models/task.py following data-model.md
- [ ] T010 Configure error handling and logging infrastructure per research.md
- [ ] T011 Setup environment configuration management in backend/src/config.py
- [ ] T012 [P] Create authentication dependency in backend/src/core/dependencies.py
- [ ] T013 Create base service layer interface in backend/src/services/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts and authenticate securely to access their personal task data.

**Independent Test**: Can create a new user account via signup endpoint, login with credentials, and receive a valid authentication token that allows access to protected endpoints.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Contract test for authentication endpoints in backend/tests/contract/test_auth.py
- [ ] T015 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [ ] T016 [P] [US1] Implement user service in backend/src/services/auth_service.py for signup business logic
- [ ] T017 [P] [US1] Implement authentication verification in backend/src/services/auth_service.py
- [ ] T018 [US1] Implement signup endpoint in backend/src/routers/auth.py with email validation
- [ ] T019 [US1] Implement login endpoint in backend/src/routers/auth.py with JWT token generation
- [ ] T020 [US1] Add request validation and error handling for auth endpoints
- [ ] T021 [US1] Add logging for authentication operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Creation and Retrieval (Priority: P1)

**Goal**: Allow authenticated users to create tasks with title and description, and retrieve paginated lists of their own tasks.

**Independent Test**: Can authenticate a user, create multiple tasks via POST endpoint, and retrieve the task list via GET endpoint with pagination.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US2] Contract test for task endpoints in backend/tests/contract/test_tasks.py
- [ ] T023 [P] [US2] Integration test for task creation and retrieval flow in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [x] T024 [P] [US2] Update task service in backend/src/services/task_service.py for creation logic
- [x] T025 [P] [US2] Update task service in backend/src/services/task_service.py for retrieval logic
- [x] T026 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py
- [x] T027 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py with pagination
- [x] T028 [US2] Implement path-token matching verification in task endpoints per spec FR-015
- [x] T029 [US2] Add request validation and error handling for task endpoints
- [x] T030 [US2] Add logging for task operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Updates and Completion (Priority: P2)

**Goal**: Allow authenticated users to modify existing tasks by updating title/description and toggling completion status.

**Independent Test**: Can create a task, update its properties via PUT endpoint, mark it complete via PATCH endpoint, and verify changes persist.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US3] Contract test for update/complete endpoints in backend/tests/contract/test_tasks.py
- [ ] T032 [P] [US3] Integration test for task updates and completion flow in backend/tests/integration/test_tasks.py

### Implementation for User Story 3

- [x] T033 [P] [US3] Add update task logic to task service in backend/src/services/task_service.py
- [x] T034 [P] [US3] Add toggle completion logic to task service in backend/src/services/task_service.py
- [x] T035 [US3] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py
- [x] T036 [US3] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/src/routers/tasks.py
- [x] T037 [US3] Implement ownership verification for update/complete operations per spec FR-015
- [x] T038 [US3] Add request validation and error handling for update/complete endpoints

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Task Deletion (Priority: P2)

**Goal**: Allow authenticated users to permanently remove tasks from their todo list.

**Independent Test**: Can create a task, delete it via DELETE endpoint, and verify it no longer appears in task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T039 [P] [US4] Contract test for delete endpoint in backend/tests/contract/test_tasks.py
- [ ] T040 [P] [US4] Integration test for task deletion flow in backend/tests/integration/test_tasks.py

### Implementation for User Story 4

- [x] T041 [P] [US4] Add delete task logic to task service in backend/src/services/task_service.py
- [x] T042 [US4] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py
- [x] T043 [US4] Implement ownership verification for delete operations per spec FR-015
- [x] T044 [US4] Add request validation and error handling for delete endpoint

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - API Documentation and Error Handling (Priority: P3)

**Goal**: Provide comprehensive API documentation and consistent error responses for all failure scenarios.

**Independent Test**: Can access documentation endpoints, browse interactive documentation, and verify error responses follow consistent JSON structure.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T045 [P] [US5] Contract test for documentation endpoints in backend/tests/contract/test_docs.py
- [ ] T046 [P] [US5] Integration test for error response consistency in backend/tests/integration/test_errors.py

### Implementation for User Story 5

- [x] T047 [P] [US5] Implement custom exception handlers for consistent error responses per research.md
- [x] T048 [US5] Add request validation error handling with consistent format per research.md
- [x] T049 [US5] Verify interactive documentation is accessible at /docs endpoint
- [x] T050 [US5] Verify alternative documentation is accessible at /redoc endpoint

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T051 [P] Documentation updates in backend/README.md with user-scoped endpoint examples
- [x] T052 [P] Update quickstart guide with new user-scoped endpoint patterns
- [x] T053 Code cleanup and refactoring across all modules
- [ ] T054 [P] Additional unit tests in backend/tests/unit/ for service layer
- [x] T055 Security hardening for user-scoped routing verification
- [x] T056 Run quickstart.md validation with updated endpoint patterns
- [ ] T057 Performance optimization for user-scoped queries
- [x] T058 Final validation of user isolation (FR-010, SC-003)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (authentication)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 (authentication and tasks)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 (authentication and tasks)
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No specific dependencies but benefits from other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together (if tests requested):
Task: "Contract test for task endpoints in backend/tests/contract/test_tasks.py"
Task: "Integration test for task creation and retrieval flow in backend/tests/integration/test_tasks.py"

# Launch all service components for User Story 2 together:
Task: "Update task service for creation logic in backend/src/services/task_service.py"
Task: "Update task service for retrieval logic in backend/src/services/task_service.py"

# Launch all endpoints for User Story 2 together:
Task: "Implement POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py"
Task: "Implement GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py with pagination"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo (MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All task endpoints use user-scoped routing: /api/{user_id}/tasks instead of /api/tasks
- User isolation enforced through path-token matching verification (user_id from JWT token must match user_id in path parameter)
- This ensures proper ownership verification per spec requirements FR-015 and FR-016
