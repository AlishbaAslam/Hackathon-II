# Data Model: Phase-III Todo AI Chatbot

**Feature**: Phase-III Todo AI Chatbot - Planning for Integration into Existing Phase-II App
**Created**: 2026-01-14

## Entity: Conversation

### Fields
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Foreign Key to User, Required)
- **created_at**: DateTime (Timestamp, Required, Default: current timestamp)
- **updated_at**: DateTime (Timestamp, Required, Default: current timestamp)

### Relationships
- **One-to-Many**: Conversation to Messages (one conversation has many messages)
- **Many-to-One**: Conversation to User (many conversations belong to one user)

### Validation Rules
- user_id must exist in Users table
- created_at and updated_at are automatically managed
- user_id cannot be modified after creation

### State Transitions
- New conversation created when user initiates chat
- updated_at modified when new messages are added to conversation

## Entity: Message

### Fields
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Foreign Key to User, Required)
- **conversation_id**: Integer (Foreign Key to Conversation, Required)
- **role**: String (Required, Values: "user" or "assistant")
- **content**: Text (Required, Max length: 10000 characters)
- **created_at**: DateTime (Timestamp, Required, Default: current timestamp)

### Relationships
- **Many-to-One**: Message to Conversation (many messages belong to one conversation)
- **Many-to-One**: Message to User (many messages belong to one user)

### Validation Rules
- conversation_id must exist in Conversations table
- role must be either "user" or "assistant"
- content must not be empty
- user_id must match the user associated with the conversation

### State Transitions
- New message created when user sends message or assistant responds
- No modifications allowed after creation (immutable log)

## Entity: Task (Existing from Phase-II)

### Fields
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Foreign Key to User, Required)
- **title**: String (Required, Max length: 255 characters)
- **description**: Text (Optional, Max length: 10000 characters)
- **completed**: Boolean (Required, Default: False)
- **created_at**: DateTime (Timestamp, Required, Default: current timestamp)
- **updated_at**: DateTime (Timestamp, Required, Default: current timestamp)

### Relationships
- **Many-to-One**: Task to User (many tasks belong to one user)

### Validation Rules
- user_id must exist in Users table
- title must not be empty
- user_id cannot be modified after creation

## Indexes

### Conversation Table
- Index on user_id for efficient user-based queries
- Composite index on (user_id, created_at) for chronological user queries

### Message Table
- Index on conversation_id for efficient conversation retrieval
- Index on user_id for user-based queries
- Composite index on (conversation_id, created_at) for chronological message retrieval
- Composite index on (user_id, conversation_id) for user-specific conversation queries

### Task Table (Existing)
- Index on user_id for efficient user-based queries
- Index on completed for filtering by status
- Composite index on (user_id, completed) for user-based status queries

## Constraints

### Referential Integrity
- All foreign key relationships enforce referential integrity
- Cascade delete on User deletion (removes all related records)
- No orphaned messages or conversations allowed

### User Isolation
- All queries must filter by user_id to ensure data isolation
- MCP tools must validate user_id matches JWT claims
- Cross-user access prevented at database and application levels

## Access Patterns

### Common Queries
1. Get all conversations for a user: `SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC`
2. Get all messages in a conversation: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC`
3. Get specific conversation: `SELECT * FROM conversations WHERE user_id = ? AND id = ?`
4. Add new message: `INSERT INTO messages (user_id, conversation_id, role, content) VALUES (?, ?, ?, ?)`