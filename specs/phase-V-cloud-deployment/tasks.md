# Tasks: Advanced Cloud-Native Todo Chatbot with Kafka, Dapr & Real-time Sync

**Feature**: Advanced Cloud-Native Todo Chatbot with Kafka, Dapr & Real-time Sync
**Created**: 2026-02-03
**Status**: Pending
**Plan**: [/mnt/d/Hackathon-II/todo-app/specs/phase-V-cloud-deployment/plan.md](file:///mnt/d/Hackathon-II/todo-app/specs/phase-V-cloud-deployment/plan.md)

## Phase 1: Setup and Environment Configuration

**Goal**: Set up the development environment and project structure for the cloud-native todo chatbot with Kafka, Dapr, and real-time sync.

- [x] T001 Create directory structure for Phase V services following the plan.md specification
- [x] T002 Set up Dapr components configuration files (kafka-pubsub, statestore, secrets, jobs) in backend/dapr/components/
- [x] T003 Configure Kafka/Redpanda connection settings for development environment
- [x] T004 Initialize Docker and Docker Compose files for local development of all services
- [x] T005 Set up Helm chart structure for Kubernetes deployment in helm/todo-chart/
- [x] T006 Configure environment variables and secrets management for all services

## Phase 2: Foundational Components and Infrastructure

**Goal**: Establish the foundational components required for all user stories, including enhanced data models and Dapr integration.

- [x] T007 [P] Extend Task model with recurring, due_at, remind_at, priority, tags fields in backend/src/models/task.py
- [x] T008 [P] Update User model with additional fields if needed in backend/src/models/user.py
- [x] T009 [P] Create EventLog model for audit trail in backend/src/models/event_log.py
- [x] T010 [P] Create Reminder model for notification scheduling in backend/src/models/reminder.py
- [x] T011 [P] Create WebSocketSession model for real-time sync in backend/src/models/websocket_session.py
- [x] T012 [P] Implement Dapr client utilities in backend/src/core/dapr_client.py
- [x] T013 Update database configuration to support new models in backend/src/core/database.py
- [x] T014 Create Kafka topic schemas and event definitions in backend/src/core/event_schemas.py
- [x] T015 Set up Dapr sidecar configurations for all services

## Phase 3: Event-Driven Task Management (User Story 1 - P1)

**Goal**: Implement the foundational event-driven architecture that enables all other advanced features.

**Independent Test**: The system can process task creation, updates, and deletions through event streams, with proper separation of concerns between services. The user can create a task and see it propagate through the system correctly.

- [x] T016 [P] [US1] Implement Kafka/Redpanda pub/sub integration in backend/src/services/task_service.py
- [x] T017 [P] [US1] Create event publisher functions for task events in backend/src/services/event_publisher.py
- [x] T018 [US1] Update task CRUD endpoints to publish events instead of direct DB operations in backend/src/routers/tasks.py
- [x] T019 [US1] Implement event subscriber pattern for task operations in backend/src/services/event_subscriber.py
- [x] T020 [US1] Create Kafka topic consumers for task-events in backend/src/services/kafka_consumer.py
- [x] T021 [US1] Integrate Dapr pub/sub for task event handling in backend/src/services/dapr_pubsub.py
- [x] T022 [US1] Test event-driven task creation flow with proper event publishing and consumption
- [x] T023 [US1] Verify all task operations generate appropriate events and propagate correctly

## Phase 4: Recurring Task Automation (User Story 2 - P1)

**Goal**: Enable automatic generation of new task instances when recurring tasks are completed.

**Independent Test**: When a user marks a recurring task as complete, the system automatically creates the next occurrence based on the recurrence pattern without user intervention.

- [x] T024 [P] [US2] Create RecurringTaskService structure in services/recurring-task-service/src/main.py
- [x] T025 [P] [US2] Implement recurrence pattern logic and calculation in services/recurring-task-service/src/services/recurrence_logic.py
- [x] T026 [US2] Create Kafka consumer for task completion events in services/recurring-task-service/src/consumers/task_completion_consumer.py
- [x] T027 [US2] Implement next occurrence generation logic in services/recurring-task-service/src/services/occurrence_generator.py
- [x] T028 [US2] Create task creation function that publishes to task-events topic in services/recurring-task-service/src/services/task_creator.py
- [x] T029 [US2] Add validation for recurrence patterns in services/recurring-task-service/src/validators/recurrence_validator.py
- [x] T030 [US2] Implement service health checks and monitoring in services/recurring-task-service/src/health.py
- [x] T031 [US2] Test recurring task completion flow with automatic next occurrence creation
- [x] T032 [US2] Verify recurrence limits and end conditions work properly

## Phase 5: Exact-Time Reminders (User Story 3 - P1)

**Goal**: Provide precise timing for task reminders using Dapr Jobs API.

**Independent Test**: The system can schedule and deliver notifications at exact times specified by the user, using reliable scheduling mechanisms.

- [x] T033 [P] [US3] Create NotificationService structure in services/notification-service/src/main.py
- [x] T034 [P] [US3] Implement Dapr Jobs API integration for scheduling reminders in services/notification-service/src/services/job_scheduler.py
- [x] T035 [US3] Create Kafka consumer for reminder scheduling events in services/notification-service/src/consumers/reminder_consumer.py
- [x] T036 [US3] Implement notification delivery mechanisms (email, push, etc.) in services/notification-service/src/services/notification_sender.py
- [x] T037 [US3] Create reminder scheduling logic with timezone handling in services/notification-service/src/services/reminder_scheduler.py
- [x] T038 [US3] Add notification channel selection and management in services/notification-service/src/services/channel_manager.py
- [x] T039 [US3] Implement retry logic for failed notifications in services/notification-service/src/services/retry_handler.py
- [x] T040 [US3] Test exact-time reminder delivery with sub-5-second variance
- [x] T041 [US3] Verify reminder cancellation when tasks are completed/deleted

## Phase 6: Real-time Multi-Device Sync (User Story 4 - P2)

**Goal**: Enable real-time synchronization of task changes across all connected devices using WebSocket.

**Independent Test**: When a user makes changes to a task on one device, those changes appear immediately on other connected devices through WebSocket connections.

- [x] T042 [P] [US4] Create WebSocketService structure in services/websocket-service/src/main.py
- [x] T043 [P] [US4] Implement WebSocket server with connection management in services/websocket-service/src/services/ws_server.py
- [x] T044 [US4] Create WebSocket connection authentication and authorization in services/websocket-service/src/middleware/auth.py
- [x] T045 [US4] Implement task update broadcaster for WebSocket connections in services/websocket-service/src/services/broadcaster.py
- [x] T046 [US4] Create Kafka consumer for task-updates topic in services/websocket-service/src/consumers/task_updates_consumer.py
- [x] T047 [US4] Implement connection persistence and reconnection handling in services/websocket-service/src/services/connection_manager.py
- [x] T048 [US4] Add message formatting for different task update types in services/websocket-service/src/services/message_formatter.py
- [x] T049 [US4] Create WebSocket client for frontend integration in frontend/hooks/useWebSocket.ts
- [x] T050 [US4] Test real-time sync with sub-500ms propagation time across multiple clients
- [x] T051 [US4] Verify WebSocket connection stability with 99% uptime

## Phase 7: Task Enhancement Features (User Story 5 - P2)

**Goal**: Add support for priorities, tags, due dates, and search/filter capabilities to tasks.

**Independent Test**: Users can set and view additional task properties like priority and tags, and can filter/search tasks based on these attributes.

- [x] T052 [P] [US5] Update frontend UI to support priority selection in frontend/components/tasks/TaskForm.tsx
- [x] T053 [P] [US5] Implement tag input component for task tagging in frontend/components/tasks/TagInput.tsx
- [x] T054 [US5] Add due date and reminder time pickers in frontend/components/tasks/DateTimePickers.tsx
- [x] T055 [US5] Create recurrence pattern configuration UI in frontend/components/tasks/RecurrenceConfig.tsx
- [x] T056 [US5] Update task list to display enhanced task properties in frontend/components/tasks/TaskList.tsx
- [x] T057 [US5] Implement search and filter functionality in frontend/hooks/useTasks.ts
- [x] T058 [US5] Add advanced filtering options in frontend/components/tasks/TaskFilters.tsx
- [x] T059 [US5] Update backend API to support querying with new parameters in backend/src/routers/tasks.py
- [x] T060 [US5] Create database indexes for enhanced query performance in backend/src/core/database.py
- [x] T061 [US5] Test task enhancement features with search/filter operations returning results in under 2 seconds

## Phase 8: Cloud-Native Deployment (User Story 6 - P3)

**Goal**: Deploy the system to Kubernetes with Dapr integration for cloud-native scalability.

**Independent Test**: The application can be successfully deployed to both local Minikube and production Kubernetes clusters with all services running properly.

- [x] T062 [P] [US6] Create Dockerfiles for all microservices in services/*/Dockerfile
- [x] T063 [P] [US6] Update Helm chart for all services in helm/todo-chart/
- [x] T064 [US6] Create Kubernetes deployment configurations for all services in k8s/
- [x] T065 [US6] Configure Dapr components for Kubernetes in k8s/dapr/
- [x] T066 [US6] Set up Kafka/Redpanda deployment in Kubernetes in k8s/kafka/
- [x] T067 [US6] Create ingress configuration for external access in k8s/ingress.yaml
- [x] T068 [US6] Implement health checks for all services in src/health.py
- [x] T069 [US6] Test deployment to Minikube with all services operational
- [x] T070 [US6] Create cloud deployment configurations for OKE in k8s/cloud/

## Phase 9: Audit and Monitoring Services

**Goal**: Implement comprehensive audit logging and monitoring capabilities.

- [x] T071 [P] Create AuditService structure in services/audit-service/src/main.py
- [x] T072 [P] Implement event logging functionality in services/audit-service/src/services/audit_logger.py
- [x] T073 Create Kafka consumer for all task events in services/audit-service/src/consumers/event_consumer.py
- [x] T074 Implement audit log storage and retrieval in services/audit-service/src/services/storage.py
- [x] T075 Add audit log API endpoints in services/audit-service/src/routers/audit.py
- [x] T076 Integrate audit service with all other services for complete logging
- [x] T077 Set up basic monitoring and logging infrastructure in k8s/monitoring/

## Phase 10: Integration and End-to-End Testing

**Goal**: Perform comprehensive testing of the integrated system to ensure all components work together.

- [x] T078 [P] Create integration tests for event-driven flows in backend/tests/test_integration.py
- [x] T079 Implement end-to-end tests for recurring task functionality
- [x] T080 Create end-to-end tests for reminder scheduling and delivery
- [x] T081 Implement real-time sync end-to-end tests
- [x] T082 Test complete user journey: task creation → real-time sync → reminder → audit log
- [x] T083 Validate all success criteria from specification are met

## Phase 11: Polish and Cross-Cutting Concerns

**Goal**: Address cross-cutting concerns and polish the implementation.

- [x] T084 Implement proper error handling and graceful degradation when services are unavailable
- [x] T085 Add comprehensive logging across all services
- [x] T086 Optimize performance based on testing results
- [x] T087 Update documentation for all new features and services
- [x] T088 Perform security review and ensure user isolation is maintained
- [x] T089 Conduct final validation against all success criteria

## Dependencies

### User Story Completion Order
1. **US1 (Event-Driven Task Management)** - Foundation for all other stories
2. **US2 (Recurring Tasks)** - Depends on US1 for event publishing
3. **US3 (Reminders)** - Depends on US1 for event handling
4. **US4 (Real-time Sync)** - Depends on US1 for task updates
5. **US5 (Task Enhancement)** - Can be developed in parallel after US1
6. **US6 (Cloud Deployment)** - Can be developed in parallel, integrates all services

### Critical Path
US1 → US2, US3, US4 (all depend on event-driven foundation)

## Parallel Execution Opportunities

### Within Each User Story
- Model creation, service implementation, and endpoint creation can often run in parallel
- Different services (recurring-task, notification, websocket) can be developed simultaneously
- Frontend and backend work can be done in parallel after API contracts are defined

### Per User Story
- **US1**: Event publisher and subscriber implementations can be parallelized
- **US2**: Recurrence logic and Kafka consumer can be developed separately
- **US3**: Job scheduler and notification sender can be parallelized
- **US4**: WebSocket server and client components can be developed in parallel
- **US5**: Frontend UI components can be built in parallel

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
- Complete US1 (Event-Driven Task Management) as the core foundation
- Implement basic US2 (Recurring Tasks) functionality
- Include basic US3 (Reminders) with simple scheduling
- Deploy to Minikube for demonstration

### Incremental Delivery
1. **Foundation**: Complete Phase 1-2 (Setup and Foundational Components)
2. **Core Features**: Complete US1-3 (Event-driven, Recurring, Reminders)
3. **Enhancements**: Add US4-5 (Real-time sync, Task enhancements)
4. **Deployment**: Complete US6 and Phase 10-11 (Cloud deployment, testing)

### Risk Mitigation
- Implement and test the event-driven architecture early (US1) as it's foundational
- Validate Dapr integration with Kafka early in the process
- Test cross-service communication thoroughly before adding complexity