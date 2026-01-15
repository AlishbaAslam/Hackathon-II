# Quickstart Guide: Phase-III Todo AI Chatbot

**Feature**: Phase-III Todo AI Chatbot - Planning for Integration into Existing Phase-II App
**Created**: 2026-01-14

## Prerequisites

Before implementing the AI chatbot feature, ensure the following prerequisites are met:

- Phase-II Todo app is fully functional with authentication
- Better Auth is properly configured with JWT support
- Neon PostgreSQL database is accessible and properly configured
- Python 3.13+ and uv package manager installed
- Node.js 18+ and npm/yarn for frontend development
- OpenRouter account with API access

## Environment Setup

### Backend Environment Variables
Create or update `.env` file in the backend directory:

```bash
# Database Configuration
NEON_DB_URL="postgresql://username:password@ep-..."

# OpenRouter Configuration
OPENROUTER_API_KEY="sk-or-v1-..."

# JWT Secret for Better Auth integration
JWT_SECRET="your-secret-key"
```

### Frontend Environment Variables
Create or update `.env.local` file in the frontend directory:

```bash
# ChatKit Domain Key (required for production)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your-domain-key"

# Backend API URL
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
```

## Implementation Steps

### Step 1: Database Setup
1. Create the Conversation and Message models based on the data-model.md
2. Run database migrations to create the new tables
3. Verify that indexes are properly created for performance

### Step 2: MCP Tools Integration
1. Implement the 5 required tools within the existing backend: add_task, list_tasks, complete_task, delete_task, update_task
2. Integrate MCP tools directly into the existing FastAPI application
3. Test the MCP tools functionality within the existing backend
4. Ensure user isolation is enforced in all tools using existing JWT validation

### Step 3: Backend Chat Endpoint
1. Create the `/api/{user_id}/chat` endpoint in FastAPI
2. Implement conversation state management
3. Integrate with OpenRouter's AsyncOpenAI client
4. Connect to MCP tools server for task operations
5. Add JWT authentication and user validation

### Step 4: Frontend Integration
1. Add ChatKit UI to the existing application
2. Implement the right-side chat widget
3. Connect to the backend chat endpoint
4. Handle authentication headers properly
5. Test responsive design across devices

### Step 5: Testing
1. Test all natural language commands work properly
2. Verify conversation persistence across sessions
3. Confirm user isolation is enforced
4. Test error handling and confirmation responses
5. Validate OpenRouter model responses

## Running the Application

### Backend (FastAPI with Integrated MCP Tools)
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
uvicorn src.main:app --reload --port 8000
```
The MCP tools are integrated directly into the main FastAPI application.

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

## API Testing

Once the backend is running, you can test the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

Expected response:
```json
{
  "conversation_id": 1,
  "response": "I've added the task 'Buy groceries' to your list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "Buy groceries"
      }
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **JWT Authentication Errors**
   - Verify JWT token is properly formatted and not expired
   - Check that user_id in JWT matches the path parameter

2. **OpenRouter Connection Issues**
   - Confirm OPENROUTER_API_KEY is correctly set
   - Verify network connectivity to OpenRouter API

3. **MCP Tools Not Responding**
   - Verify that the integrated MCP tools are properly registered in the FastAPI application
   - Check that tool configurations are correct within the backend

4. **Database Connection Problems**
   - Verify database URL and credentials
   - Confirm required tables exist and are properly indexed

## Production Deployment

1. Configure domain allowlist for ChatKit in production
2. Set up proper environment variables for production
3. Ensure SSL/TLS is configured for all endpoints
4. Set up monitoring for API usage and response times
5. Implement proper logging and error tracking