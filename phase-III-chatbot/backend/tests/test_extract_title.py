#!/usr/bin/env python3
"""
Test script to verify the updated _extract_task_title function works correctly
"""

import re

def _extract_task_title(message: str) -> str:
    """
    Updated version of the _extract_task_title function for testing
    """
    message_lower = message.lower().strip()

    # Enhanced update patterns to handle various update/rename/change commands
    update_patterns = [
        # Pattern for "update task [id] title [new title]" - handles colon, quotes, extra spaces
        r"update\s+task\s+\d+\s+title\s*[,:]*\s*(.+)$",
        # Pattern for "change task [id] title [new title]" - handles colon, quotes, extra spaces
        r"change\s+task\s+\d+\s+title\s*[,:]*\s*(.+)$",
        # Pattern for "rename task [id] to [new title]" - handles colon, quotes, extra spaces
        r"rename\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
        # Pattern for "update task [id] to [new title]" - handles colon, quotes, extra spaces
        r"update\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
        # Pattern for "change task [id] to [new title]" - handles colon, quotes, extra spaces
        r"change\s+task\s+\d+\s+to\s+[\"':]?\s*(.+)$",
        # General pattern for update/rename/change to [new title]
        r"(?:update|change|rename|modify)\s+.*?\s+to\s+[\"':]?\s*(.+)$",
        # Pattern for commands with colons (e.g., "update task 4: buy groceries")
        r"(?:update|change|rename|modify)\s+task\s+\d+\s*[:]\s*(.+)$",
        # Pattern for commands with quotes (e.g., "update task 4 to 'buy groceries'")
        r"(?:update|change|rename|modify)\s+.*?\s+(?:to|title)\s+['\"](.+?)['\"]",
    ]

    for pattern in update_patterns:
        match = re.search(pattern, message_lower)
        if match:
            title = match.group(1).strip()
            # Remove potential trailing punctuation or extra words
            title = re.sub(r'[.,!?;]+$', '', title).strip()
            # Remove quotes if present (handles both opening and closing quotes)
            title = re.sub(r'^["\'](.+?)["\']$', r'\1', title).strip()
            # Remove remaining trailing quote if not paired
            title = re.sub(r'["\']$', '', title).strip()

            # Remove any leading command remnants but be careful not to remove legitimate content
            title = re.sub(r'^(?:to|the|a|an)\s+', '', title).strip()

            if title and title not in ["me", "it", "them", "that", "this", "there", "here", "to", "the", "a", "an"]:
                return title.capitalize()

    # Patterns for extracting task titles for creation (keep existing patterns)
    patterns = [
        r"add a task (?:to |)(.*)",
        r"create a task (?:to |)(.*)",
        r"add task (?:to |)(.*)",
        r"create task (?:to |)(.*)",  # Added to handle "create task clean room"
        r"remember to (.*)",
        r"need to (.*)",
        r"have to (.*)",
        r"add (?:a |)(.*)",
        r"create (?:a |)(.*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            title = match.group(1).strip()
            # Clean up the title - be more specific to avoid removing parts of legitimate words
            title = re.sub(r'\b(?:that|i)\b', '', title).strip()  # Remove 'that' and 'i' when standalone
            # Remove leading articles or pronouns that might be left
            title = re.sub(r'^(?:the|a|an)\s+', '', title).strip()

            # Clean up extra whitespace that might have been left by removals
            title = re.sub(r'\s+', ' ', title).strip()

            if title:
                return title.capitalize()

    # If no pattern matched, return the original message as title
    # but only if it seems like a reasonable task (not too long, not containing commands)
    if len(message.split()) <= 10 and not any(cmd in message_lower for cmd in ["list", "show", "delete", "complete", "update", "change", "rename", "modify"]):
        return message.strip()

    # Fallback: ask for clarification if it's an update command but title couldn't be extracted clearly
    if any(update_cmd in message_lower for update_cmd in ["update", "change", "rename", "modify"]) and any(digit in message for digit in "0123456789"):
        return None

    return None

# Test cases for the updated function
test_cases = [
    # Original problematic cases
    ("change task 4 title : buy cat for me", "Buy cat for me"),
    ("update task 4 title buy car for me", "Buy car for me"),

    # Additional update/rename/change cases
    ("update task 1 to buy groceries", "Buy groceries"),
    ("change task 2 to finish report", "Finish report"),
    ("rename task 3 to pay bills", "Pay bills"),
    ("update task 5 title go to gym", "Go to gym"),
    ("change task 6 title call mom", "Call mom"),
    ("rename task 7 to schedule meeting", "Schedule meeting"),
    ("update task 8 to 'work on project'", "Work on project"),
    ("change task 9 title: walk the dog", "Walk the dog"),
    ("rename task 10 to : finish homework", "Finish homework"),

    # Edge cases
    ("update task 1", None),  # No title provided
    ("change task 2 title", None),  # No title provided
    ("update task 3 to", None),  # No title provided

    # Add task cases (should still work)
    ("add a task to buy milk", "Buy milk"),
    ("create task clean room", "Clean room"),
    ("remember to call dad", "Call dad"),
]

print("Testing the updated _extract_task_title function:")
print("=" * 60)

all_passed = True
for i, (input_msg, expected) in enumerate(test_cases, 1):
    result = _extract_task_title(input_msg)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    if result != expected:
        all_passed = False
    print(f"{i:2}. Input: '{input_msg}'")
    print(f"    Expected: {expected}, Got: {result} - {status}")
    print()

print("=" * 60)
if all_passed:
    print("🎉 All tests passed!")
else:
    print("❌ Some tests failed.")