---
name: chatkit-ui-setup
description: A skill for integrating OpenAI ChatKit frontend, domain allowlist, environment keys, backend connection, and responsive chat UI. Always uses Context7 MCP for documentation access. Follows SDD workflow methodology.
version: 1.0.0
---

# ChatKit UI Setup Skill

## Purpose

The chatkit-ui-setup skill is designed to help users integrate OpenAI ChatKit frontend components, configure domain allowlists, set up environment keys, establish backend connections, and implement responsive chat UI elements. It ensures proper configuration and secure integration while following SDD methodology.

## When to Use

Use this skill when you need to:

- **Integrate OpenAI ChatKit** into your Next.js application
  - User: "Please set up the OpenAI ChatKit UI and connect it to our backend chat endpoint"
  - Assistant: Uses the skill to properly configure the ChatKit frontend with domain allowlists and connect it to the backend endpoint

- **Configure domain keys** and environment variables
  - User: "How do I set up the NEXT_PUBLIC_OPENAI_DOMAIN_KEY and configure the domain allowlist?"
  - Assistant: Uses the skill to handle the domain configuration and environment variable setup

- **Establish secure frontend-backend connections**
  - User: "Connect the ChatKit UI to our FastAPI backend securely"
  - Assistant: Uses the skill to ensure proper API integration with authentication

- **Implement responsive chat UI** elements
  - User: "Create a responsive chat interface using ChatKit components"
  - Assistant: Uses the skill to implement responsive design patterns with ChatKit

## Process Steps

1. **Analyze Integration Requirements**
   - Identify the specific ChatKit components needed
   - Determine domain allowlist requirements
   - Define environment variable needs
   - Plan backend connection strategy

2. **Research with Context7 MCP**
   - Use Context7 MCP to access latest ChatKit documentation
   - Look up best practices for domain configuration
   - Verify current standards for secure API connections
   - Check responsive design patterns for chat interfaces

3. **Configure Environment Variables**
   - Set up NEXT_PUBLIC_OPENAI_DOMAIN_KEY
   - Configure domain allowlist settings
   - Define backend API endpoints
   - Secure sensitive configuration values

4. **Implement Frontend Integration**
   - Install and configure ChatKit components
   - Set up domain allowlist validation
   - Connect to backend endpoints
   - Implement responsive design patterns

5. **Establish Backend Connection**
   - Configure CORS settings for domain allowlist
   - Implement secure API authentication
   - Test connection between frontend and backend
   - Validate error handling paths

6. **Validate Implementation**
   - Test domain allowlist functionality
   - Verify secure connection to backend
   - Confirm responsive behavior across devices
   - Validate error handling and user feedback

7. **Review and Iterate**
   - Check against quality criteria
   - Validate with stakeholders if needed
   - Update based on feedback

## Output Format

ChatKit UI setups created with this skill follow a standardized format:

```typescript
// Environment variables (.env.local)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your-domain-key"
NEXT_PUBLIC_BACKEND_URL="https://your-backend-url.com"
NEXT_PUBLIC_CHATKIT_API_KEY="your-chatkit-api-key"

// Frontend component (pages/index.tsx or app/page.tsx)
"use client";

import { ChatInterface } from "@openai/chatkit";

const ChatPage = () => {
  return (
    <div className="chat-container">
      <ChatInterface
        domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
        // Additional configuration options
      />
    </div>
  );
};

export default ChatPage;

// Backend connection configuration (lib/api.ts)
const createChatSession = async (userId: string) => {
  // Logic to connect to backend chat endpoint
  // Secure authentication and validation
};

// Domain allowlist configuration (middleware or API routes)
const validateDomainAccess = (req, res, next) => {
  // Logic to validate domain access based on allowlist
};
```

## Quality Criteria

ChatKit UI setups created with this skill must meet the following criteria:

- **Domain Allowlist**: Properly configured domain validation and security
- **Environment Security**: Secure handling of API keys and sensitive data
- **Backend Connection**: Reliable and secure connection to backend services
- **Responsive Design**: Properly implemented responsive UI across all device sizes
- **Performance**: Optimized loading times and smooth user interactions
- **Security**: Proper authentication and data protection measures
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Accessibility**: Compliance with WCAG accessibility standards
- **Maintainability**: Clean, well-documented code that's easy to update
- **Compatibility**: Works across different browsers and platforms

## Context7 MCP Integration

This skill mandates the use of Context7 MCP for:

- Accessing up-to-date documentation on OpenAI ChatKit
- Retrieving best practices for domain configuration
- Validating secure API integration patterns
- Checking responsive design guidelines
- Ensuring compatibility with current frontend frameworks