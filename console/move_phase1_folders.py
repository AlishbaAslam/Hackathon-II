#!/usr/bin/env python3
"""
Script to move all phase 1 folders from history/prompts to a new console folder.
"""
import os
import shutil
from pathlib import Path

def move_phase1_folders():
    """
    Move all phase 1 folders from history/prompts to a new console folder.
    """
    # Define source and destination paths
    source_dir = Path("history/prompts")
    dest_dir = source_dir / "console"

    # Create the console directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {dest_dir}")

    # Identify phase 1 folders (assuming they have "phase" or "1" in their names)
    # Or possibly folders related to phase 1 work - let me look for common patterns
    phase1_patterns = ["phase1", "001", "phase-1", "phase_1"]

    # Get all directories in history/prompts
    all_dirs = [d for d in source_dir.iterdir() if d.is_dir()]

    # Filter for potential phase 1 folders
    phase1_dirs = []
    for d in all_dirs:
        dir_name = d.name.lower()
        # Check if it looks like a phase 1 folder
        if any(pattern in dir_name for pattern in phase1_patterns) or dir_name.startswith("001-"):
            phase1_dirs.append(d)

    # If no phase 1 folders identified by pattern, I'll assume you mean specific folders
    # Since the original request mentioned "4 phase 1 folders", let me move the most likely candidates
    if not phase1_dirs:
        # Let's assume the 4 folders in history/prompts are the ones to move (excluding console if it already existed)
        phase1_dirs = [d for d in all_dirs if d.name != "console"]

    moved_folders = []

    for folder in phase1_dirs:
        if folder.name == "console":
            continue  # Skip the console directory itself

        dest_path = dest_dir / folder.name

        # Move the folder
        shutil.move(str(folder), str(dest_path))
        moved_folders.append(folder.name)
        print(f"Moved: {folder.name} -> {dest_dir}/{folder.name}")

    print(f"\nTotal folders moved: {len(moved_folders)}")
    for folder in moved_folders:
        print(f"- {folder}")

if __name__ == "__main__":
    move_phase1_folders()