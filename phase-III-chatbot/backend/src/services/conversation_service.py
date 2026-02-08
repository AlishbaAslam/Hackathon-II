from typing import Optional, List
from sqlmodel import Session, select, func
from datetime import datetime
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate


def create_conversation(*, session: Session, conversation_create: ConversationCreate) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        session: Database session
        conversation_create: Conversation creation data

    Returns:
        Created Conversation object
    """
    conversation = Conversation.model_validate(conversation_create)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation_by_id(*, session: Session, conversation_id: int, user_id: str) -> Optional[Conversation]:
    """
    Get a specific conversation by ID for a user (enforcing user isolation).

    Args:
        session: Database session
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user who owns the conversation

    Returns:
        Conversation object if found and owned by user, None otherwise
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_uuid
    )
    conversation = session.exec(statement).first()
    return conversation


def get_conversations_by_user(*, session: Session, user_id: str) -> List[Conversation]:
    """
    Get all conversations for a user, ordered by most recent update.

    Args:
        session: Database session
        user_id: ID of the user whose conversations to retrieve

    Returns:
        List of Conversation objects
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Conversation).where(
        Conversation.user_id == user_uuid
    ).order_by(Conversation.updated_at.desc())
    conversations = session.exec(statement).all()
    return conversations


def update_conversation_timestamp(*, session: Session, conversation: Conversation) -> Conversation:
    """
    Update the updated_at timestamp of a conversation.

    Args:
        session: Database session
        conversation: Conversation to update

    Returns:
        Updated Conversation object
    """
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def create_message(*, session: Session, message_create: MessageCreate) -> Message:
    """
    Create a new message in a conversation.

    Args:
        session: Database session
        message_create: Message creation data

    Returns:
        Created Message object
    """
    from uuid import UUID

    # Create a dict copy to avoid modifying the original parameter
    message_data = message_create.model_dump()

    # Convert string user_id to UUID if needed for model validation
    if isinstance(message_data.get('user_id'), str):
        message_data['user_id'] = UUID(message_data['user_id'])

    message = Message.model_validate(message_data)
    session.add(message)
    session.commit()
    session.refresh(message)

    # Update the conversation's updated_at timestamp
    from ..models.conversation import Conversation
    conversation = session.get(Conversation, message.conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

    return message


def get_messages_by_conversation(*, session: Session, conversation_id: int, user_id: str) -> List[Message]:
    """
    Get all messages for a conversation, enforcing user isolation.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user who owns the conversation

    Returns:
        List of Message objects
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_uuid
    ).order_by(Message.created_at.asc())
    messages = session.exec(statement).all()
    return messages


def get_recent_messages_for_user(*, session: Session, user_id: str, limit: int = 50) -> List[Message]:
    """
    Get recent messages for a user across all conversations.

    Args:
        session: Database session
        user_id: ID of the user whose messages to retrieve
        limit: Maximum number of messages to return

    Returns:
        List of Message objects
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Message).where(
        Message.user_id == user_uuid
    ).order_by(Message.created_at.desc()).limit(limit)
    messages = session.exec(statement).all()
    return messages