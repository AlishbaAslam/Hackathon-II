"""Chat Router for AI-Powered Conversations

This module implements the /api/{user_id}/chat endpoint for handling natural language
messages and returning AI-generated responses.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.dependencies import get_current_user
from ..models.user import User
from ..core.database import get_db
from ..services.conversation_service_async import (
    get_conversation_by_id as get_conversation_by_id_async,
    create_conversation as create_conversation_async,
    get_conversations_by_user as get_conversations_by_user_async,
    create_message as create_message_async,
    get_messages_by_conversation as get_messages_by_conversation_async
)
from ..models.conversation import ConversationCreate
from ..models.message import MessageCreate
from ..services.agent_service import get_agent_service


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: int
    response: str
    tool_calls: list = []


router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Handle natural language messages and return AI-generated responses.

    Args:
        user_id: ID of the user from the path parameter
        request: Chat request containing conversation_id and message
        current_user: Current authenticated user from JWT token
        session: Async database session

    Returns:
        ChatResponse containing conversation_id, response, and tool_calls
    """
    # Verify that the user_id in the path matches the user from the JWT token
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in path does not match authenticated user"
        )

    # Get or create a conversation
    conversation = None
    if request.conversation_id:
        # Try to get existing conversation for this user
        conversation = await get_conversation_by_id_async(
            session=session,
            conversation_id=request.conversation_id,
            user_id=user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found for user {user_id}"
            )
    else:
        # Create a new conversation
        conversation_data = ConversationCreate(user_id=user_id)
        conversation = await create_conversation_async(
            session=session,
            conversation_create=conversation_data
        )

    # Create the user message in the database
    user_message = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    created_user_message = await create_message_async(
        session=session,
        message_create=user_message
    )

    # Get the conversation history to provide context to the agent
    conversation_history = await get_messages_by_conversation_async(
        session=session,
        conversation_id=conversation.id,
        user_id=user_id
    )

    # Prepare history for the agent (excluding the current message we just added)
    history_for_agent = []
    for msg in conversation_history[:-1] if conversation_history else []:  # Exclude the current user message
        history_for_agent.append({
            "role": msg.role,
            "content": msg.content
        })

    # Process the message with the AI agent
    agent_svc = get_agent_service()
    result = await agent_svc.process_message(
        user_id=user_id,
        message_content=request.message,
        conversation_history=history_for_agent,
        session=session
    )

    # Create the assistant's response message in the database
    assistant_message = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=result["response"]
    )
    created_assistant_message = await create_message_async(
        session=session,
        message_create=assistant_message
    )

    # Return the response
    return ChatResponse(
        conversation_id=conversation.id,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )