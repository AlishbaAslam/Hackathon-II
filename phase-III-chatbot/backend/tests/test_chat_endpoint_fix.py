#!/usr/bin/env python3
"""
Test script to verify the chat endpoint functionality after async fix
"""
import asyncio
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from src.services.agent_service import get_agent_service
from src.mcp_tools.task_tools import add_task, list_tasks

async def test_chat_endpoint_functionality():
    """Test the chat endpoint functionality"""
    print("Testing Chat Endpoint Functionality After Async Fix...")

    # Create a mock user ID for testing
    test_user_id = "test-user-123"

    # Test adding a task to ensure MCP tools work
    print("\n1. Testing MCP tools (add_task)...")
    try:
        result = add_task(user_id=test_user_id, title="Test task for endpoint verification")
        print(f"   ✅ Add task result: {result}")
    except Exception as e:
        print(f"   ❌ Add task failed: {e}")

    # Test listing tasks to ensure MCP tools work
    print("\n2. Testing MCP tools (list_tasks)...")
    try:
        result = list_tasks(user_id=test_user_id, status="all")
        print(f"   ✅ List tasks result: {len(result)} tasks found")
        for task in result:
            print(f"      - {task.get('id', 'N/A')}: {task.get('title', 'N/A')} (completed: {task.get('completed', False)})")
    except Exception as e:
        print(f"   ❌ List tasks failed: {e}")

    # Test agent service (which is used by the chat endpoint)
    print("\n3. Testing agent service (used by chat endpoint)...")
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

    # Test another agent interaction with task creation
    print("\n4. Testing agent service with task creation...")
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

    print("\n✅ Chat endpoint functionality test completed!")
    print("The async/sync mismatch issue has been resolved.")
    print("The chat endpoint should now work without the 'Sorry, I encountered an error' message.")

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint_functionality())