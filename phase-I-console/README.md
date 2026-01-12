# Todo Console App

A comprehensive in-memory todo console application built with Python 3.13+ featuring intelligent task management capabilities.

## Features

- **Add Task** - Create tasks with title, description, priority, tags, due dates, due times, and recurrence patterns
- **View Tasks** - See all tasks with full metadata (Priorities, Tags, Due Dates/Times, Recurrence)
- **Update Task** - Modify specific fields using a dedicated sub-menu
- **Delete Task** - Remove tasks by ID
- **Mark Complete** - Toggle task completion status (with automatic recurrence handling)
- **Search & Filter** - Find tasks by keyword, status, priority, or tags
- **Sort View** - Reorder by due date, priority, or alphabetically
- **Intelligent Recurrence** - Automate routine tasks (Daily, Weekly, Monthly) with automatic generation of next instances
- **Precise Scheduling** - Set due times (HH:MM or AM/PM) and receive console alerts
- **Batch Rescheduling** - Quickly move backlog (overdue) tasks to Today or specific date/time
- **Colorful Interface** - Enhanced UX with ANSI colors, emojis, and imminent deadline alerts
- **Time Format Support** - Accept both 24-hour (HH:MM) and 12-hour (H:MM AM/PM) time formats
- **Overdue Task Management** - Automatic detection and intelligent rescheduling of overdue tasks
- **Imminent Deadline Notifications** - Background thread monitors and alerts for upcoming deadlines

## Setup

This project uses [UV](https://github.com/astral-sh/uv) for dependency management.

### Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Initialize the project

```bash
uv sync
```

## Running the Application

```bash
uv run python -m src.main
```

Or alternatively:

```bash
cd src
python main.py
```

## Usage

When you run the application, you'll see a colorful menu with emojis:

```
========================================
    📝 TODO CONSOLE APP
========================================

  1. ➕ Add Task
  2. 📋 View Tasks
  3. ✏️  Update Task
  4. 🗑️  Delete Task
  5. ✅ Mark Complete
  6. 🔍 Search & Filter
  7. 🔃 Sort View
  8. 💡 Intelligence
  9. 🚪 Exit

----------------------------------------
Enter your choice (1-9):
```

The **Intelligence** menu (option 8) provides advanced features:
- Auto Reschedule: Move all overdue tasks to today
- Batch Reschedule Overdue to Specific Date/Time: Move overdue tasks to a custom date/time

### Example: Adding a Task with Advanced Features

```
Enter your choice (1-9): 1

➕ Add Task
--------------------
Enter title: Morning Yoga
Enter description (optional): 20 min session
Priority: [1] High, [2] Medium, [3] Low
Select priority (default: 2): 1
Enter tags (comma-separated, max 3): health, routine
Enter due date (YYYY-MM-DD, optional): 2026-01-02
Enter due time (HH:MM 24h or H:MM AM/PM, optional): 7:00 AM
Recurrence: [1] None, [2] Daily, [3] Weekly, [4] Monthly
Select recurrence (default: 1): 2
✅ Task added successfully! (ID: 1)

Enter your choice (1-9): 2
📋 Your Tasks
--------------------
[⬜] 1. (High) Morning Yoga #health #routine 📅 2026-01-02 7:00 AM 🔃 Daily
```

### Example: Using Search & Filter

```
Enter your choice (1-9): 6
🔍 Search & Filter
1. Keyword Search
2. Filter by Status
3. Filter by Priority
4. Filter by Tag
5. Back to Main Menu
Select option: 1
Enter keyword: yoga
[⬜] 1. (High) Morning Yoga #health #routine 📅 2026-01-02 7:00 AM 🔃 Daily
```

### Example: Using Intelligence Features

```
Enter your choice (1-9): 8
💡 Intelligence
1. Auto Reschedule
2. Batch Reschedule Overdue to Specific Date/Time
3. Back to Main Menu
Select option: 1
Auto rescheduling all overdue tasks...
✅ 0 tasks rescheduled.
```

## Project Structure

```
todo-console-app/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── models.py        # Task dataclass
│   ├── todo_service.py  # Business logic (CRUD, recurrence, scheduling)
│   └── cli.py           # Console interface (menus, input handling, colors)
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── specs/               # Specification history (Phase-I, Intermediate, Advanced)
│   ├── 001-todo-cli/
│   ├── 002-todo-intermediate/
│   └── 001-todo-advanced/
├── history/             # PHR records
├── tests/               # Unit and integration tests
├── pyproject.toml       # Project dependencies and metadata
├── uv.lock              # Lock file for dependency management
├── .venv/               # Virtual environment (if using UV)
├── .gitignore           # Git ignore patterns
├── CLAUDE.md            # Claude Code instructions
└── README.md            # This file
```

## Requirements Met

- All 5 core features implemented (Add, View, Update, Delete, Mark Complete)
- Advanced features implemented (Search, Filter, Sort, Recurring Tasks, Due Times, Notifications)
- In-memory storage (no files, no database)
- Input validation and error handling
- Clean, modular Python code with separation of concerns
- PEP 8 compliant with type hints
- Support for multiple time formats (24-hour and 12-hour AM/PM)
- Intelligent task management (auto-rescheduling, overdue handling)
- Colorful console interface with ANSI colors and emojis
- Background notification system for imminent deadlines
- Comprehensive task metadata (priorities, tags, due dates/times, recurrence)
- Proper handling of recurring tasks with automatic instance generation
- Task filtering and sorting capabilities
- Intelligent rescheduling of overdue tasks

## License

MIT
