# Feature Specification: The Evolution of Todo – Intermediate Level (Organization & Usability)

**Feature Branch**: `002-todo-intermediate`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "The Evolution of Todo – Intermediate Level (Organization & Usability). Focus: Priorities, categories/tags, search, filter, and task sorting features."

## Clarifications

### Session 2025-12-31

- Q: How should the CLI handle updating the new task metadata (priority, due date, tags) for existing tasks? → A: Field-specific sub-menu
- Q: What should be the default sort order when sorting by Due Date? → A: Oldest first (chronological)
- Q: Should there be a limit on the number of tags assigned to a single task? → A: Fixed limit (max 3 tags)
- Q: How should the system handle invalid due date strings during interactive input? → A: Immediate re-prompt until valid or empty
- Q: Should task search and tag filtering be case-sensitive or case-insensitive? → A: Case-insensitive

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Organization (Priorities & Tags) (Priority: P1)

As a user, I want to assign priorities and labels to my tasks so that I can organize my work and focus on what's important.

**Why this priority**: Organization is the core theme of the Intermediate level. Priorities and tags are the primary metadata that enable all subsequent search, filter, and sort features.

**Independent Test**: Can be fully tested by creating a task and assigning it a priority (High, Medium, or Low) and a label (Work, Home, or custom tag), and then verifying these details are visible in the task list.

**Acceptance Scenarios**:

1. **Given** the user is adding a new task, **When** prompted for priority, **Then** they can select from "High", "Medium", or "Low" (defaulting to Medium if skipped).
2. **Given** a task is being created or updated, **When** prompted for a label/tag, **Then** the user can enter a custom string (e.g., "Work", "Home") or leave it empty.
3. **Given** tasks with priorities and tags exist, **When** viewing the task list, **Then** these attributes are clearly displayed alongside the title and status.

---

### User Story 2 - Search Tasks (Priority: P1)

As a user, I want to search for tasks by keyword so that I can quickly find specific items in a long list.

**Why this priority**: Search is a fundamental usability feature for any list-based application once the volume of data grows beyond a handful of items.

**Independent Test**: Add several tasks with different keywords in titles and descriptions, then search for a specific word and verify that only matching tasks are displayed.

**Acceptance Scenarios**:

1. **Given** multiple tasks exist, **When** the user enters a search keyword, **Then** only tasks whose title or description contains the keyword (case-insensitive) are displayed.
2. **Given** a search is performed, **When** no tasks match the keyword, **Then** a clear message "No matching tasks found" is displayed.

---

### User Story 3 - Filter and Sort Tasks (Priority: P2)

As a user, I want to filter and sort my task list so that I can view my work in the order that makes most sense for my current context.

**Why this priority**: Filters and sorting turn a flat list into a manageable dashboard, allowing users to slice their data by status or priority.

**Independent Test**: Create tasks with different priorities and completion statuses, then apply a filter (e.g., "High Priority only") followed by a sort (e.g., "Alphabetical") and verify the view reflects both.

**Acceptance Scenarios**:

1. **Given** the task list view, **When** the user applies a priority filter, **Then** only tasks matching that specific priority are shown.
2. **Given** the task list view, **When** the user selects "Sort by Priority", **Then** tasks are displayed in order: High → Medium → Low (or vice versa).
3. **Given** a list of tasks with varied titles, **When** the user selects "Sort Alphabetically", **Then** tasks are ordered A-Z by title.

---

### User Story 4 - Due Dates (Priority: P2)

As a user, I want to assign due dates to tasks so that I can track deadlines and sort my work by urgency.

**Why this priority**: While the user prompt mentioned sorting by "due date", it didn't explicitly ask for adding the field. However, sorting by due date implies its existence.

**Independent Test**: Assign a due date to a task and verify it is displayed and can be used for sorting.

**Acceptance Scenarios**:

1. **Given** a task is being created/updated, **When** prompted for a due date, **Then** the user can enter a date in YYYY-MM-DD format (or leave optional).
2. **Given** tasks with due dates exist, **When** sorting by due date, **Then** tasks are displayed from earliest to latest (or vice versa).

---

### Edge Cases

- What happens if a user enters an invalid date format? (Answer: Immediate re-prompt until valid).
- How are tasks without a due date handled when sorting by due date? (Informed Guess: They appear at the end of the list).
- How does the system handle searching for special characters or empty search strings? (Answer: Case-insensitive match; empty string matches all).
- What happens if the user tries to add more than 3 tags? (Answer: Only the first 3 are accepted or user is re-prompted).
- What happens if the user tries to apply multiple conflicting filters?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow assigning one of three priority levels to a task: High, Medium, or Low.
- **FR-002**: System MUST allow adding up to 3 tags/labels as text strings to a task.
- **FR-003**: System MUST support an optional `due_date` field stored as a date object.
- **FR-004**: System MUST provide a search interface that filters the current view based on a case-insensitive keyword match in `title` or `description`.
- **FR-005**: System MUST allow filtering the task list by `status` (Complete/Incomplete), `priority`, and `tag` (case-insensitive).
- **FR-006**: System MUST allow sorting the task list by `due_date` (Oldest First by default), `priority` (High > Medium > Low), and `alphabetical` (title A-Z).
- **FR-007**: System MUST validate date inputs to ensure they follow the `YYYY-MM-DD` format, re-prompting immediately on failure.
- **FR-008**: System MUST maintain backward compatibility with Phase-I tasks (existing tasks should default to Medium priority, no tags, no due date).
- **FR-009**: System MUST provide a field-specific sub-menu for updating task metadata.

### Key Entities

- **Task (Enhanced)**:
  - `id` (integer): Unique identifier (Phase-I)
  - `title` (string): Required (Phase-I)
  - `description` (string): Optional (Phase-I)
  - `completed` (boolean): Completion status (Phase-I)
  - `priority` (enum/string): High, Medium (default), Low
  - `tags` (list of strings): Optional labels (Max 3)
  - `due_date` (date/string): Optional deadline (YYYY-MM-DD)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can assign a priority and tag to a task in under 15 seconds.
- **SC-002**: Search results for a keyword across 50 tasks return in under 500ms.
- **SC-003**: Sorting a list of 100 tasks by priority or name is instantaneous (<100ms).
- **SC-004**: All Phase-I functionality remains 100% operational after the update.
- **SC-005**: 100% of invalid date entries are caught and handled with an immediate re-prompt.

## Assumptions

- We will use the standard `datetime` library for handling due dates.
- For the CLI, we will expand the menu to include "Search/Filter" and "Sort" sub-menus or options.
- "Medium" will be the default priority for all new and existing tasks.
- Multiple tags will be comma-separated during input and limited to 3.
- All search and filter operations are case-insensitive.

## Out of Scope

- Persistence to disk (Advanced Level).
- Natural language parsing for dates (e.g., "next Tuesday").
- Automated reminders or notifications.
- Recurring tasks logic (Advanced Level).
