"""Console interface for the todo application."""

import sys
import threading
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo_service import TodoService, TodoServiceError


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLINK = "\033[5m"  # Added blink for imminent alerts

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def colorize(text: str, color: str) -> str:
    """Apply color to text.

    Args:
        text: The text to colorize.
        color: ANSI color code.

    Returns:
        Colorized text with reset code.
    """
    return f"{color}{text}{Colors.RESET}"


class NotificationThread(threading.Thread):
    """Background thread to monitor upcoming tasks and set alert flags."""

    def __init__(self, service: TodoService) -> None:
        super().__init__(daemon=True)
        self.service = service
        self.stop_event = threading.Event()
        self.upcoming_alerts: list = []

    def run(self) -> None:
        """Continuously check for alerts every 30 seconds."""
        for _ in range(2):  # Delay first check slightly to let app start
            if self.stop_event.is_set(): return
            time.sleep(1)

        while not self.stop_event.is_set():
            self.upcoming_alerts = self.service.get_upcoming_alerts(window_minutes=15)
            # Sleep in small increments to remain responsive to stop_event
            for _ in range(30):
                if self.stop_event.is_set(): return
                time.sleep(1)


def display_menu(alerts: list = None) -> None:
    """Display the main menu options.

    Args:
        alerts: Optional list of imminent tasks to highlight.
    """
    if alerts:
        print()
        print(colorize("🔔 IMMINENT ALERTS", Colors.BOLD + Colors.BRIGHT_RED + Colors.BLINK))
        for task in alerts:
            due_info = f"{task.due_date} {convert_to_12h_format(task.due_time) if task.due_time else ''}"
            print(colorize(f"   - {task.title} (Due: {due_info})", Colors.BRIGHT_RED))
            # Trigger terminal bell for high priority imminent alerts
            if task.priority == "High":
                print("\a", end="")

    print()
    print(colorize("=" * 40, Colors.BRIGHT_CYAN))
    print(colorize("    📝 TODO CONSOLE APP", Colors.BOLD + Colors.BRIGHT_YELLOW))
    print(colorize("=" * 40, Colors.BRIGHT_CYAN))
    print()
    print(colorize("  1. ➕ Add Task", Colors.CYAN))
    print(colorize("  2. 📋 View Tasks", Colors.CYAN))
    print(colorize("  3. ✏️  Update Task", Colors.CYAN))
    print(colorize("  4. 🗑️  Delete Task", Colors.CYAN))
    print(colorize("  5. ✅ Mark Complete", Colors.CYAN))
    print(colorize("  6. 🔍 Search & Filter", Colors.BRIGHT_BLUE))
    print(colorize("  7. 🔃 Sort View", Colors.BRIGHT_BLUE))
    print(colorize("  8. 💡 Intelligence", Colors.BRIGHT_MAGENTA))
    print(colorize("  9. 🚪 Exit", Colors.BRIGHT_RED))
    print()
    print(colorize("-" * 40, Colors.DIM))


def get_task_input() -> tuple[str, str, str, list[str]]:
    """Get task details: title, description, priority, and tags.

    Returns:
        Tuple of (title, description, priority, tags).
    """
    while True:
        title = input(colorize("Enter title: ", Colors.BRIGHT_GREEN)).strip()
        if title:
            break
        print(colorize("Error: Title cannot be empty. Please try again.", Colors.BRIGHT_RED))

    description = input(colorize("Enter description (optional): ", Colors.BRIGHT_GREEN)).strip()

    print(colorize("Priority: [1] High, [2] Medium, [3] Low", Colors.DIM))
    p_choice = input(colorize("Select priority (default: 2): ", Colors.BRIGHT_GREEN)).strip()
    p_map = {"1": "High", "2": "Medium", "3": "Low"}
    priority = p_map.get(p_choice, "Medium")

    tags_input = input(colorize("Enter tags (comma-separated, max 3): ", Colors.BRIGHT_GREEN)).strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

    return title, description, priority, tags


def get_task_id(prompt: str) -> int:
    """Get and validate a task ID from user.

    Args:
        prompt: The prompt to display.

    Returns:
        Valid positive integer, or 0 if empty (cancel).
    """
    while True:
        try:
            task_id_str = input(colorize(prompt, Colors.BRIGHT_GREEN)).strip()
            if not task_id_str:
                return 0
            task_id = int(task_id_str)
            if task_id > 0:
                return task_id
            print(colorize("Error: Please enter a positive number.", Colors.BRIGHT_RED))
        except ValueError:
            print(colorize("Error: Please enter a valid number.", Colors.BRIGHT_RED))


def run_add_task(service: TodoService) -> None:
    """Run the Add Task workflow.

    Args:
        service: The TodoService instance.
    """
    print()
    print(colorize("➕ Add Task", Colors.BOLD + Colors.CYAN))
    print(colorize("-" * 20, Colors.DIM))

    title, description, priority, tags = get_task_input()

    while True:
        due_date = input(colorize("Enter due date (YYYY-MM-DD, optional): ", Colors.BRIGHT_GREEN)).strip()
        if not due_date or service.validate_date(due_date):
            break
        print(colorize("Error: Invalid date format. Please use YYYY-MM-DD.", Colors.BRIGHT_RED))

    due_time = None
    if due_date:
        while True:
            due_time = input(colorize("Enter due time (HH:MM 24h or H:MM AM/PM, optional): ", Colors.BRIGHT_GREEN)).strip()
            if not due_time or service.validate_time(due_time):
                break
            print(colorize("Error: Invalid time format. Use HH:MM (24-hour) or H:MM AM/PM (12-hour) format.", Colors.BRIGHT_RED))

    print(colorize("Recurrence: [1] None, [2] Daily, [3] Weekly, [4] Monthly", Colors.DIM))
    r_choice = input(colorize("Select recurrence (default: 1): ", Colors.BRIGHT_GREEN)).strip()
    r_map = {"1": None, "2": "Daily", "3": "Weekly", "4": "Monthly"}
    recurrence = r_map.get(r_choice)

    try:
        task = service.add_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date if due_date else None,
            due_time=due_time if due_time else None,
            recurrence=recurrence
        )
        print(colorize(f"✅ Task added successfully! (ID: {task.id})", Colors.BRIGHT_GREEN))
    except TodoServiceError as e:
        print(colorize(f"Error: {e}", Colors.BRIGHT_RED))


from datetime import datetime


def convert_to_12h_format(time_str: str) -> str:
    """Convert 24-hour time format to 12-hour AM/PM format.

    Args:
        time_str: Time string in HH:MM format (24-hour)

    Returns:
        Time string in 12-hour AM/PM format
    """
    if not time_str or not time_str.strip():
        return ""

    try:
        hour, minute = time_str.split(":")
        hour = int(hour)
        minute = int(minute)

        if hour == 0:
            # 00:00 → 12:00 AM
            return f"12:{minute:02d} AM"
        elif 1 <= hour <= 11:
            # 01:00–11:59 → AM
            return f"{hour}:{minute:02d} AM"
        elif hour == 12:
            # 12:00 → 12:00 PM
            return f"12:{minute:02d} PM"
        else:  # 13-23
            # 13:00–23:59 → subtract 12 → PM
            return f"{hour - 12}:{minute:02d} PM"
    except (ValueError, IndexError):
        # If there's an error in parsing, return the original string
        return time_str


def display_tasks_custom(tasks: list) -> None:
    """Shared display logic for any task list."""
    print()
    if not tasks:
        print(colorize("No tasks to display matching criteria.", Colors.DIM))
        return

    for task in tasks:
        status_emoji = "✅" if task.completed else "⬜"
        status_color = Colors.BRIGHT_GREEN if task.completed else Colors.DIM
        status_text = colorize(f"[{status_emoji}]", status_color)

        p_colors = {"High": Colors.BRIGHT_RED, "Medium": Colors.BRIGHT_YELLOW, "Low": Colors.BRIGHT_BLUE}
        p_text = colorize(f"({task.priority})", p_colors.get(task.priority, Colors.DIM))

        title_color = Colors.WHITE if task.completed else Colors.BRIGHT_WHITE
        title_text = colorize(task.title, title_color)

        # Check if task is overdue (not completed and due date/time has passed)
        is_overdue = False
        if task.due_date and not task.completed:
            try:
                due_dt_str = f"{task.due_date} {task.due_time if task.due_time else '00:00'}"
                due_dt = datetime.strptime(due_dt_str, "%Y-%m-%d %H:%M")
                now = datetime.now()
                if due_dt < now:
                    is_overdue = True
            except ValueError:
                pass  # Invalid date/time format, skip overdue check

        # Add [INCOMPLETE] indicator for overdue tasks (in red)
        overdue_indicator = colorize(" [INCOMPLETE]", Colors.BRIGHT_RED) if is_overdue else ""

        tags_text = colorize(f" #{' #'.join(task.tags)}", Colors.CYAN) if task.tags else ""
        due_text = ""
        if task.due_date:
            time_part = f" {convert_to_12h_format(task.due_time)}" if task.due_time else ""
            recur_part = f" 🔃 {task.recurrence}" if task.recurrence else ""
            due_text = colorize(f" 📅 {task.due_date}{time_part}{recur_part}", Colors.MAGENTA)

        print(f"{status_text} {colorize(f'{task.id}.', Colors.YELLOW)} {p_text} {title_text}{overdue_indicator}{tags_text}{due_text}")
        if task.description:
            print(colorize(f"    {task.description}", Colors.DIM))


def run_view_tasks(service: TodoService) -> None:
    """Run the View Tasks workflow."""
    print()
    print(colorize("📋 Your Tasks", Colors.BOLD + Colors.CYAN))
    print(colorize("-" * 20, Colors.DIM))
    display_tasks_custom(service.get_all_tasks())


def run_search_filter_menu(service: TodoService) -> None:
    """Sub-menu for Search and Filter."""
    while True:
        print(f"\n{colorize('🔍 Search & Filter', Colors.BOLD + Colors.CYAN)}")
        print("1. Keyword Search")
        print("2. Filter by Status")
        print("3. Filter by Priority")
        print("4. Filter by Tag")
        print("5. Back to Main Menu")

        try:
            choice = int(input(colorize("Select option: ", Colors.BRIGHT_GREEN)).strip())
            if choice == 5: break

            results = []
            if choice == 1:
                kw = input(colorize("Enter keyword: ", Colors.BRIGHT_GREEN)).strip()
                results = service.search_tasks(kw)
            elif choice == 2:
                s_choice = input(colorize("Status ([1] Complete, [2] Incomplete): ", Colors.BRIGHT_GREEN)).strip()
                results = service.filter_tasks(status=(s_choice == "1"))
            elif choice == 3:
                print(colorize("Priority: [1] High, [2] Medium, [3] Low", Colors.DIM))
                p_val = input(colorize("Select priority: ", Colors.BRIGHT_GREEN)).strip()
                p_map = {"1": "High", "2": "Medium", "3": "Low"}
                if p_val in p_map: results = service.filter_tasks(priority=p_map[p_val])
            elif choice == 4:
                tag = input(colorize("Enter tag: ", Colors.BRIGHT_GREEN)).strip()
                results = service.filter_tasks(tag=tag)

            if choice in [1, 2, 3, 4]:
                display_tasks_custom(results)
        except ValueError:
            print(colorize("Error: Invalid selection.", Colors.BRIGHT_RED))


def run_sort_menu(service: TodoService) -> None:
    """Sub-menu for Sorting."""
    while True:
        print(f"\n{colorize('🔃 Sort Tasks', Colors.BOLD + Colors.CYAN)}")
        print("1. Sort by Priority (High to Low)")
        print("2. Sort Alphabetically (A-Z)")
        print("3. Sort by Due Date (Oldest First)")
        print("4. Back to Main Menu")

        try:
            choice = int(input(colorize("Select option: ", Colors.BRIGHT_GREEN)).strip())
            if choice == 4: break

            results = []
            if choice == 1: results = service.sort_tasks("priority")
            elif choice == 2: results = service.sort_tasks("alphabetical")
            elif choice == 3: results = service.sort_tasks("due_date")

            if results:
                display_tasks_custom(results)
        except ValueError:
            print(colorize("Error: Invalid selection.", Colors.BRIGHT_RED))


def run_update_task(service: TodoService) -> None:
    """Run the Update Task workflow."""
    print()
    print(colorize("✏️  Update Task", Colors.BOLD + Colors.CYAN))
    print(colorize("-" * 20, Colors.DIM))

    task_id = get_task_id("Enter task ID to update (or Enter to cancel): ")
    if not task_id: return

    task = service.get_task(task_id)
    if task is None:
        print(colorize(f"Error: Task with ID {task_id} not found.", Colors.BRIGHT_RED))
        return

    print(f"\nEditing Task {task_id}: {colorize(task.title, Colors.BOLD)}")
    print("1. Title")
    print("2. Description")
    print("3. Priority")
    print("4. Tags")
    print("5. Due Date")
    print("6. Due Time")
    print("7. Recurrence")
    print("8. Cancel")

    try:
        choice = int(input(colorize("Select field to update: ", Colors.BRIGHT_GREEN)).strip())
        if choice == 8: return

        update_args = {}
        if choice == 1:
            val = input(colorize(f"New title (Current: {task.title}): ", Colors.BRIGHT_GREEN)).strip()
            if val: update_args["title"] = val
        elif choice == 2:
            val = input(colorize(f"New description (Current: {task.description or '(none)'}): ", Colors.BRIGHT_GREEN)).strip()
            update_args["description"] = val if val else None
        elif choice == 3:
            print(colorize("Priority: [1] High, [2] Medium, [3] Low", Colors.DIM))
            p_val = input(colorize(f"New priority (Current: {task.priority}): ", Colors.BRIGHT_GREEN)).strip()
            p_map = {"1": "High", "2": "Medium", "3": "Low"}
            if p_val in p_map: update_args["priority"] = p_map[p_val]
        elif choice == 4:
            val = input(colorize(f"New tags (Current: {', '.join(task.tags) or '(none)'}): ", Colors.BRIGHT_GREEN)).strip()
            update_args["tags"] = service.validate_tags([t.strip() for t in val.split(",") if t.strip()] if val else [])
        elif choice == 5:
            while True:
                val = input(colorize(f"New due date YYYY-MM-DD (Current: {task.due_date or '(none)'}): ", Colors.BRIGHT_GREEN)).strip()
                if not val or service.validate_date(val):
                    update_args["due_date"] = val if val else None
                    break
                print(colorize("Error: Invalid date format.", Colors.BRIGHT_RED))
        elif choice == 6:
            while True:
                val = input(colorize(f"New due time (HH:MM 24h or H:MM AM/PM) (Current: {task.due_time or '(none)'}): ", Colors.BRIGHT_GREEN)).strip()
                if not val or service.validate_time(val):
                    update_args["due_time"] = val if val else None
                    break
                print(colorize("Error: Invalid time format. Use HH:MM (24-hour) or H:MM AM/PM (12-hour) format.", Colors.BRIGHT_RED))
        elif choice == 7:
            print(colorize("Recurrence: [1] None, [2] Daily, [3] Weekly, [4] Monthly", Colors.DIM))
            r_val = input(colorize(f"New recurrence (Current: {task.recurrence or 'None'}): ", Colors.BRIGHT_GREEN)).strip()
            r_map = {"1": None, "2": "Daily", "3": "Weekly", "4": "Monthly"}
            if r_val in r_map:
                update_args["recurrence"] = r_map[r_val]

        if update_args and service.update_task(task_id, **update_args):
            print(colorize("✅ Task updated successfully!", Colors.BRIGHT_GREEN))
    except (ValueError, TodoServiceError) as e:
        print(colorize(f"Error: {e}", Colors.BRIGHT_RED))


def run_delete_task(service: TodoService) -> None:
    """Run the Delete Task workflow."""
    print()
    print(colorize("🗑️  Delete Task", Colors.BOLD + Colors.CYAN))
    print(colorize("-" * 20, Colors.DIM))

    task_id = get_task_id("Enter task ID to delete: ")
    if task_id and service.delete_task(task_id):
        print(colorize("🗑️  Task deleted successfully!", Colors.BRIGHT_GREEN))
    elif task_id:
        print(colorize(f"Error: Task with ID {task_id} not found.", Colors.BRIGHT_RED))


def run_mark_complete(service: TodoService) -> None:
    """Run the Mark Complete workflow."""
    print()
    print(colorize("✅ Mark Complete", Colors.BOLD + Colors.CYAN))
    print(colorize("-" * 20, Colors.DIM))

    task_id = get_task_id("Enter task ID to mark complete: ")
    if task_id and service.toggle_complete(task_id):
        task = service.get_task(task_id)
        status = "complete" if task.completed else "incomplete"
        emoji = "✅" if task.completed else "⬜"
        print(colorize(f"{emoji} Task {task_id} is now {status}.", Colors.BRIGHT_GREEN))
    elif task_id:
        print(colorize(f"Error: Task with ID {task_id} not found.", Colors.BRIGHT_RED))


def run_intelligence_menu(service: TodoService) -> None:
    """Sub-menu for Intelligent features."""
    while True:
        print(f"\n{colorize('💡 Intelligence', Colors.BOLD + Colors.BRIGHT_MAGENTA)}")
        print("1. Auto Reschedule")
        print("2. Batch Reschedule Overdue to Specific Date/Time")
        print("3. Back to Main Menu")

        try:
            choice_str = input(colorize("Select option: ", Colors.BRIGHT_GREEN)).strip()
            if not choice_str: continue
            choice = int(choice_str)

            if choice == 3: break
            if choice == 1:
                today = datetime.now().strftime("%Y-%m-%d")
                print(colorize(f"Auto rescheduling all overdue tasks...", Colors.DIM))
                count = service.reschedule_overdue_tasks(today)
                print(colorize(f"✅ {count} tasks rescheduled.", Colors.BRIGHT_GREEN))

                # Ask if user wants to view the updated tasks
                view_updated = input(colorize("View updated tasks? (y/N): ", Colors.BRIGHT_GREEN)).strip().lower()
                if view_updated in ['y', 'yes']:
                    display_tasks_custom(service.get_all_tasks())
            elif choice == 2:
                datetime_input = input(colorize("Enter new datetime (YYYY-MM-DD HH:MM): ", Colors.BRIGHT_GREEN)).strip()
                if datetime_input:
                    try:
                        # Validate datetime format
                        datetime.strptime(datetime_input, "%Y-%m-%d %H:%M")
                        print(colorize(f"Rescheduling all overdue tasks to {datetime_input}...", Colors.DIM))
                        count = service.batch_reschedule_overdue(datetime_input)
                        print(colorize(f"✅ {count} tasks rescheduled.", Colors.BRIGHT_GREEN))

                        # Ask if user wants to view the updated tasks
                        view_updated = input(colorize("View updated tasks? (y/N): ", Colors.BRIGHT_GREEN)).strip().lower()
                        if view_updated in ['y', 'yes']:
                            display_tasks_custom(service.get_all_tasks())
                    except ValueError:
                        print(colorize("Error: Invalid datetime format. Use YYYY-MM-DD HH:MM.", Colors.BRIGHT_RED))
            else:
                print(colorize("Error: Please select 1-3.", Colors.BRIGHT_RED))
        except ValueError:
            print(colorize("Error: Invalid selection.", Colors.BRIGHT_RED))


def run_cli() -> None:
    """Run the main CLI loop."""
    service = TodoService()

    # Start notification thread
    notifier = NotificationThread(service)
    notifier.start()

    try:
        while True:
            display_menu(notifier.upcoming_alerts)
            try:
                choice_str = input(colorize("Enter your choice (1-9): ", Colors.BRIGHT_GREEN)).strip()
                if not choice_str: continue
                choice = int(choice_str)

                if choice == 1: run_add_task(service)
                elif choice == 2: run_view_tasks(service)
                elif choice == 3: run_update_task(service)
                elif choice == 4: run_delete_task(service)
                elif choice == 5: run_mark_complete(service)
                elif choice == 6: run_search_filter_menu(service)
                elif choice == 7: run_sort_menu(service)
                elif choice == 8: run_intelligence_menu(service)
                elif choice == 9:
                    print(colorize("\nGoodbye! Thanks for using Todo Console App 👋", Colors.BRIGHT_YELLOW))
                    break
                else:
                    print(colorize("Error: Please select 1-9.", Colors.BRIGHT_RED))
            except ValueError:
                print(colorize("Error: Please enter a valid number.", Colors.BRIGHT_RED))
    finally:
        notifier.stop_event.set()
        notifier.join(timeout=2.0)
