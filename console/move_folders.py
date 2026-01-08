#!/usr/bin/env python3
"""
Script to move specific folders from history/prompts to a new console folder.
Moves 'todo-cli', '001-todo-advanced', and '002-todo-intermediate' folders.
"""
import os
import shutil
from pathlib import Path

def main():
    # Define source and destination paths
    source_dir = Path("history/prompts")
    dest_dir = source_dir / "console"

    # Create the console directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {dest_dir}")

    # Define the specific folders to move
    folders_to_move = ["todo-cli", "001-todo-advanced", "002-todo-intermediate"]

    for folder_name in folders_to_move:
        source_path = source_dir / folder_name
        dest_path = dest_dir / folder_name

        # Check if the source folder exists before moving
        if source_path.exists():
            # Move the folder
            shutil.move(str(source_path), str(dest_path))
            print(f"Moved: {folder_name}")
        else:
            print(f"Folder does not exist: {folder_name}")

if __name__ == "__main__":
    main()