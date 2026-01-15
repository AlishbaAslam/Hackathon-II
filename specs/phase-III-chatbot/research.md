# Research Summary: Phase-III Todo AI Chatbot

**Feature**: Phase-III Todo AI Chatbot - Planning for Integration into Existing Phase-II App
**Created**: 2026-01-14

## Research Task 0.1: OpenRouter Integration Best Practices

### Decision: AsyncOpenAI Client Configuration for OpenRouter
**Rationale**: OpenRouter provides an OpenAI-compatible API that allows using the standard OpenAI SDK with different models and pricing structures. The AsyncOpenAI client enables efficient async operations in FastAPI applications.

**Implementation Details**:
- Use AsyncOpenAI client with OpenRouter base URL: `https://openrouter.ai/api/v1`
- Set API key from environment variable: `OPENROUTER_API_KEY`
- Configure model to use: `deepseek/deepseek-r1-0528:free` for cost-free operations
- Set appropriate timeouts and retry logic

**Alternatives Considered**:
- Direct OpenAI API: Would require OpenAI key and paid usage
- Self-hosted models: Higher complexity and resource requirements
- Other AI providers: Limited compatibility with OpenAI Agents SDK

## Research Task 0.2: MCP SDK Implementation Patterns

### Decision: Integrated MCP Tools within Existing Backend
**Rationale**: Integrating MCP tools directly within the existing FastAPI backend maintains a single codebase, simplifies deployment, and reduces operational complexity. This approach leverages existing infrastructure and authentication systems.

**Implementation Details**:
- Implement MCP tools as part of the existing FastAPI application
- Use existing database connections and authentication middleware
- Leverage existing JWT validation for user isolation
- Maintain the same deployment and scaling characteristics as the main application
- Share common utilities and services between existing endpoints and MCP tools

**Alternatives Considered**:
- Standalone MCP server: Would require separate deployment and management
- HTTP-based tools: Would add network overhead to tool calls
- Direct database access: Would bypass proper tool abstraction

## Research Task 0.3: ChatKit Production Deployment

### Decision: Domain Allowlist Configuration Process
**Rationale**: OpenAI requires domain allowlisting for security when using ChatKit in production environments. This ensures that only authorized domains can access the ChatKit service.

**Implementation Details**:
- Deploy frontend to production domain first
- Add domain to OpenAI's domain allowlist in security settings
- Obtain NEXT_PUBLIC_OPENAI_DOMAIN_KEY after domain registration
- Configure environment variable in deployment pipeline
- Test locally and in production environments

**Production Deployment Steps**:
1. Deploy frontend to production URL (e.g., `https://myapp.vercel.app`)
2. Register domain at `https://platform.openai.com/settings/organization/security/domain-allowlist`
3. Add the provided domain key to `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` environment variable
4. Redeploy with updated configuration

**Alternatives Considered**:
- Custom chat interface: Would require more development time
- Third-party chat widgets: Would add external dependencies
- Self-hosted chat solution: Would increase infrastructure complexity

## Additional Research Findings

### OpenAI Agents SDK with OpenRouter
- The OpenAI Agents SDK can work with OpenRouter by configuring the client appropriately
- Tool calling functionality is preserved when using OpenRouter-compatible models
- Response quality varies by model but the free models offer acceptable performance for task management

### MCP Tools Best Practices
- Tools should be stateless and rely on external storage (database) for persistence
- User isolation must be enforced in each tool through JWT validation from existing Better Auth system
- Proper error handling and logging are essential for debugging AI interactions
- Tools should return structured responses that the agent can interpret effectively
- Integration within existing backend allows sharing of authentication and database connection logic

### Database Connection for MCP Tools
- MCP tools leverage the same database connections as the main application
- Connection pooling is shared with existing FastAPI application to avoid resource duplication
- Transaction handling should ensure data consistency across operations
- MCP tools utilize existing database configuration from environment variables
- User isolation is enforced through existing JWT validation middleware