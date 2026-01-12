# Implementation Plan: 002-todo-intermediate

**Branch**: `002-todo-intermediate` | **Date**: 2025-12-31 | **Spec**: [specs/002-todo-intermediate/spec.md](../spec.md)

## Summary

This plan outlines the implementation of the Intermediate Level features for the Todo Console App. We will enhance the existing `Task` model with priorities, tags, and due dates, and implement search/filter/sort logic within the `TodoService` and a new sub-menu structure in the `CLI`.

## Technical Context

- **Language/Version**: Python 3.13+
- **Primary Dependencies**: Standard library (`dataclasses`, `datetime`, `typing`)
- **Storage**: In-memory (List of `Task` objects in `TodoService`)
- **Architecture**: Modular Monolith (Models, Service, Interface)
- **Constraints**:
    - Backward compatibility with Phase-I tasks.
    - Standard library only.
    - CLI-only menu-driven interface.

## Constitution Check

- **Spec-Driven**: All features map to `002-todo-intermediate/spec.md`.
- **Backward Compatibility**: Existing `Task` model will be updated with optional/default values for new fields.
- **Maintainability**: Logic will be kept modular within the service.
- **Simplicity**: No complex indexing; linear scan (O(N)) is acceptable for small/medium in-memory lists.

## Project Structure

```text
src/
├── models.py        # Updated Task dataclass
├── todo_service.py  # New search/filter/sort logic
├── cli.py           # New sub-menus and display logic
└── main.py          # Entry point (no changes needed)

specs/002-todo-intermediate/
├── spec.md          # Approved specification
├── plan.md          # This file
├── checklists/
│   ├── requirements.md
│   └── architecture.md
└── tasks.md         # Next step
```

## Architecture Decisions

### 1. Priority System
**Decision**: Use an `Enum` or constant-driven string approach (High, Medium, Low) rather than a numeric scale.
**Rationale**: Simpler CLI interaction; users prefer named categories over arbitrary numbers for basic todo lists. "Medium" remains the default.

### 2. Tag/Category Design
**Decision**: User-defined free-text tags.
**Rationale**: Maximum flexibility. Users can input labels like "work" or "home" dynamically. Internally stored as a `List[str]` in the `Task` object.

### 3. Search & Filter Implementation
**Decision**: Linear scan (iterating through the list).
**Rationale**: Since it's in-memory and the expected task count is low (<1000), O(N) filtering is highly efficient and keeps the code simple and readable.

### 4. Sorting Algorithm
**Decision**: Standard Python `list.sort()` with `lambda` keys.
**Rationale**: Python's Timsort is stable and performant. `priority` sorting will use a mapping dictionary (`{'High': 0, 'Medium': 1, 'Low': 2}`).

## Implementation Approach

1.  **Phase 1: Model Update**: Update `Task` in `models.py` with `priority`, `tags`, and `due_date`.
2.  **Phase 2: Service Logic**:
    - Add `search_tasks(keyword)` to `TodoService`.
    - Add `filter_tasks(status, priority, tag)` to `TodoService`.
    - Add `sort_tasks(criterion)` to `TodoService`.
3.  **Phase 3: CLI Enhancement**:
    - Update `Add` and `Update` flows to capture new metadata.
    - Implement a "Search & Filter" sub-menu.
    - Implement a "Sort View" sub-menu.
    - Update the task display format to show the new attributes.

## Testing Strategy

- **Unit Tests**:
    - Verify filtering results with overlapping criteria (e.g., Status=Complete AND Priority=High).
    - Verify sorting order for priorities (High always appears before Medium).
    - Verify date validation logic (Accepts YYYY-MM-DD, rejects others).
- **Manual CLI Validation**:
    - Add a task with all metadata and view it.
    - Add a task with minimal metadata and view it (checking defaults).
    - Perform a keyword search multiple times.
- **Edge cases**:
    - Sorting an empty list.
    - Searching with an empty string.
    - Updating a task with invalid date format.
