#!/usr/bin/env python3
"""
Script to manually update the database schema with missing columns.
This addresses the issue where the Task model has new fields but the database doesn't.
"""

import asyncio
from sqlalchemy import text
from src.core.database import engine, sync_engine


async def add_missing_columns():
    """Add missing columns to the tasks table."""
    async with engine.begin() as conn:
        # Add due_date column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE
            """))
            print("Added due_date column to tasks table")
        except Exception as e:
            print(f"Could not add due_date column: {e}")

        # Add priority column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20)
            """))
            print("Added priority column to tasks table")
        except Exception as e:
            print(f"Could not add priority column: {e}")

        # Add tags column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags VARCHAR(500)
            """))
            print("Added tags column to tasks table")
        except Exception as e:
            print(f"Could not add tags column: {e}")

        # Add is_recurring column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE
            """))
            print("Added is_recurring column to tasks table")
        except Exception as e:
            print(f"Could not add is_recurring column: {e}")

        # Add recurrence_pattern column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20)
            """))
            print("Added recurrence_pattern column to tasks table")
        except Exception as e:
            print(f"Could not add recurrence_pattern column: {e}")

        # Add remind_at column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS remind_at TIMESTAMP WITH TIME ZONE
            """))
            print("Added remind_at column to tasks table")
        except Exception as e:
            print(f"Could not add remind_at column: {e}")

        # Add parent_task_id column
        try:
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS parent_task_id UUID REFERENCES tasks(id)
            """))
            print("Added parent_task_id column to tasks table")
        except Exception as e:
            print(f"Could not add parent_task_id column: {e}")

    await engine.dispose()


if __name__ == "__main__":
    print("Updating database schema with missing columns...")
    asyncio.run(add_missing_columns())
    print("Schema update completed!")