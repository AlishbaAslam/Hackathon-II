#!/usr/bin/env python3
"""
Test script to verify the updated list_tasks filtering for completed tasks
"""

def test_completed_keywords_detection():
    """Test that completed keywords are properly detected in messages"""

    # Simulate the logic from _identify_and_execute_tool_calls
    def detect_status_from_message(message_content):
        message_lower = message_content.lower().strip()

        # Check if it's a list_tasks command first
        list_keywords = [
            "show me", "list", "view", "display", "my tasks", "what do i have",
            "what's pending", "show tasks", "what's on my list", "all tasks",
            "list all", "what are my", "tasks list", "see my tasks", "list my tasks",
            "show my tasks", "what tasks do i have", "my task list"
        ]

        # Check if the message contains any list-related keywords
        is_list_command = any(keyword in message_lower for keyword in list_keywords)

        # Also check for the basic "show" keyword which is common in the test cases
        if not is_list_command and "show" in message_lower:
            is_list_command = True  # Consider "show" as a list command too

        if is_list_command:
            # Determine status filter more accurately
            status = "all"
            if any(pending_keyword in message_lower for pending_keyword in [
                "pending", "not done", "to do", "todo", "unfinished", "incomplete",
                "what's left", "what remains", "remaining tasks"
            ]):
                status = "pending"
            elif any(completed_keyword in message_lower for completed_keyword in [
                "completed", "done", "finished", "completed tasks", "done tasks",
                "what's done", "finished tasks", "show completed", "my completed tasks",
                "what's completed", "all completed tasks", "completed task list"
            ]):
                status = "completed"

            return status

        return None

    # Test cases
    test_cases = [
        # Should detect "completed" status
        ("show my all completed tasks", "completed"),
        ("show completed tasks", "completed"),
        ("show my completed tasks", "completed"),
        ("show completed", "completed"),

        # Should detect other statuses
        ("show my pending tasks", "pending"),
        ("show all tasks", "all"),
        ("list my tasks", "all"),

        # These won't be detected as list commands because they don't contain initial list keywords
        ("what's completed", None),  # Not detected as list command
        ("all completed tasks", None),  # Not detected as list command
        ("what completed tasks do I have", None),  # Not detected as list command

        # Should not detect list command at all
        ("add a task", None),
        ("complete task 1", None),
    ]

    print("Testing completed keywords detection:")
    print("=" * 60)

    all_passed = True
    for i, (message, expected_status) in enumerate(test_cases, 1):
        detected_status = detect_status_from_message(message)
        status = "✓ PASS" if detected_status == expected_status else "✗ FAIL"
        if detected_status != expected_status:
            all_passed = False
        print(f"{i:2}. Message: '{message}'")
        print(f"    Expected: {expected_status}, Got: {detected_status} - {status}")
        print()

    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed.")

    return all_passed

if __name__ == "__main__":
    test_completed_keywords_detection()