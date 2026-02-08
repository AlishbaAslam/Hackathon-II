#!/usr/bin/env python3
"""
Test script to verify the chatbot functionality
"""
import asyncio
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from services.agent_service import get_agent_service
from mcp_tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task

async def test_chatbot_functionality():
    """Test the chatbot functionality"""
    print("Testing Chatbot Functionality...")

    # Create a mock user ID for testing
    test_user_id = "test-user-123"

    # Test adding a task
    print("\n1. Testing add_task...")
    try:
        result = add_task(user_id=test_user_id, title="Test task from chatbot")
        print(f"   ✅ Add task result: {result}")
    except Exception as e:
        print(f"   ❌ Add task failed: {e}")

    # Test listing tasks
    print("\n2. Testing list_tasks...")
    try:
        result = list_tasks(user_id=test_user_id, status="all")
        print(f"   ✅ List tasks result: {len(result)} tasks found")
        for task in result:
            print(f"      - {task.get('id', 'N/A')}: {task.get('title', 'N/A')} (completed: {task.get('completed', False)})")
    except Exception as e:
        print(f"   ❌ List tasks failed: {e}")

    # Test agent service
    print("\n3. Testing agent service...")
    try:
        agent_service = get_agent_service()
        result = await agent_service.process_message(
            user_id=test_user_id,
            message_content="Show me my tasks",
            conversation_history=[]
        )
        print(f"   ✅ Agent response: {result['response'][:100]}...")
        print(f"   ✅ Tool calls made: {len(result['tool_calls'])}")
    except Exception as e:
        print(f"   ❌ Agent service failed: {e}")

    # Test another agent interaction
    print("\n4. Testing agent service with task addition...")
    try:
        agent_service = get_agent_service()
        result = await agent_service.process_message(
            user_id=test_user_id,
            message_content="Add a task to buy groceries",
            conversation_history=[]
        )
        print(f"   ✅ Agent response: {result['response'][:100]}...")
        print(f"   ✅ Tool calls made: {len(result['tool_calls'])}")
    except Exception as e:
        print(f"   ❌ Agent service failed: {e}")

    # Test listing tasks again to see the new task
    print("\n5. Testing list_tasks after adding new task...")
    try:
        result = list_tasks(user_id=test_user_id, status="all")
        print(f"   ✅ List tasks result: {len(result)} tasks found")
        for task in result:
            print(f"      - {task.get('id', 'N/A')}: {task.get('title', 'N/A')} (completed: {task.get('completed', False)})")
    except Exception as e:
        print(f"   ❌ List tasks failed: {e}")

    print("\n✅ Chatbot functionality test completed!")

if __name__ == "__main__":
    asyncio.run(test_chatbot_functionality())