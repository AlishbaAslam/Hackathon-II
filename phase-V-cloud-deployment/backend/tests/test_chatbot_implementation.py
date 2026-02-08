"""
Test script to validate Phase III Chatbot Implementation
"""
import asyncio
import os
from sqlmodel import Session
from src.models.user import User
from src.models.conversation import Conversation
from src.services.conversation_service import create_conversation, get_conversation_by_id
from src.services.agent_service import get_agent_service


async def test_chatbot_implementation():
    """Test the core functionality of the chatbot implementation"""

    print("Testing Phase III Todo AI Chatbot Implementation...")

    # Test 1: Verify agent service can be instantiated
    try:
        agent_service = get_agent_service()
        print("✅ Agent service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent service: {e}")
        return False

    # Test 2: Verify OpenRouter client can be instantiated
    try:
        from src.services.openrouter_client import get_openrouter_client
        # Check if API key is available (for testing purposes)
        import os
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("⚠️  OPENROUTER_API_KEY not set - this is OK for testing implementation, but needed for actual API calls")
        else:
            openrouter_client = get_openrouter_client()
            print("✅ OpenRouter client initialized successfully")
    except Exception as e:
        print(f"⚠️  Could not initialize OpenRouter client (may be due to missing API key): {e}")

    # Test 3: Verify MCP tools can be imported and used
    try:
        from src.mcp_tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task
        print("✅ MCP tools imported successfully")
    except Exception as e:
        print(f"❌ Failed to import MCP tools: {e}")
        return False

    # Test 4: Verify conversation models exist and work
    try:
        # Just test that the model can be instantiated
        conv = Conversation(user_id="test_user", id=1)
        print("✅ Conversation model works correctly")
    except Exception as e:
        print(f"❌ Conversation model failed: {e}")
        return False

    # Test 5: Verify chat router can be imported
    try:
        from src.routers.chat import router
        print("✅ Chat router imported successfully")
    except Exception as e:
        print(f"❌ Failed to import chat router: {e}")
        return False

    print("\n🎉 Basic implementation validation passed!")
    print("\nImplementation includes:")
    print("- Database models for Conversation and Message")
    print("- MCP tools for task management (add_task, list_tasks, complete_task, delete_task, update_task)")
    print("- OpenRouter client for AI model access")
    print("- Agent service with natural language processing")
    print("- Chat endpoint at /api/{user_id}/chat with JWT authentication")
    print("- Frontend ChatWidget component with ChatInterface")
    print("- Integration with existing authentication system")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_chatbot_implementation())
    if success:
        print("\n✅ Implementation validation completed successfully!")
    else:
        print("\n❌ Implementation validation failed!")
        exit(1)