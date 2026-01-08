#!/usr/bin/env python3
"""
Script to move specified folders and files into a new 'console' folder.
"""

import os
import shutil


def move_to_console():
    """Move specified folders and files into a new 'console' folder."""

    # Define the items to move
    items_to_move = [
        "src",
        "tests",
        ".venv",
        "README.md",
        "pyproject.toml",
        "uv.lock",
        ".gitignore",
        "move_folders",
        "move_phase1_folders",
        "move_specs_folders"
    ]

    # Create console folder if it doesn't exist
    console_dir = "console"
    if not os.path.exists(console_dir):
        os.makedirs(console_dir)
        print(f"Created directory: {console_dir}")

    # Track successfully moved items
    moved_items = []

    # Move each item if it exists
    for item in items_to_move:
        if os.path.exists(item):
            try:
                shutil.move(item, console_dir)
                moved_items.append(item)
                print(f"Moved: {item} -> {console_dir}/{item}")
            except Exception as e:
                print(f"Error moving {item}: {str(e)}")
        else:
            print(f"Warning: {item} does not exist, skipping...")

    print(f"\nTotal items moved: {len(moved_items)}")
    print("Successfully moved items:")
    for item in moved_items:
        print(f"  - {item}")


if __name__ == "__main__":
    move_to_console()