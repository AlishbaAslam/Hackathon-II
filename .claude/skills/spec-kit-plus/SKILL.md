# Spec Kit Plus (SDD) Skill for Full-Stack Todo App

## Overview
This skill enables agents (Spec Architect, Frontend UI, Backend Engineer, Auth Integrator) to manage, create, update, and validate specifications in a modular, chainable, and reusable way. It follows the spec-driven development workflow (Specify → Plan → Tasks → Implement) and ensures alignment with project constitution and consistency across all feature, API, database, and UI specifications.

## Purpose
- Enable spec-driven development for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all features follow the spec → plan → tasks → implement workflow
- Maintain consistency across frontend, backend, database, and authentication specifications
- Validate specifications against project constitution and requirements

## Workflow Stages

### 1. Specification Creation/Update (`specify`)
- Create or update feature specifications in `specs/[feature]/spec.md`
- Include user stories with priorities (P1, P2, etc.)
- Define acceptance criteria for each user story
- Document edge cases and error scenarios
- Ensure alignment with project constitution

### 2. Clarification (`clarify`)
- Identify underspecified areas in specifications
- Ask targeted clarification questions
- Record answers back into the spec's Clarifications section
- Resolve ambiguous requirements before planning

### 3. Planning (`plan`)
- Create architecture decisions with trade-offs
- Design module structure and data model
- Document API endpoints and database schemas
- Include security considerations and authentication flows
- Save to `specs/[feature]/plan.md`

### 4. Task Generation (`tasks`)
- Generate actionable task breakdown organized by user story
- Include dependencies between tasks
- Assign priorities to each task
- Consider integration points between frontend and backend
- Save to `specs/[feature]/tasks.md`

### 5. Implementation (`implement`)
- Execute tasks following the plan
- Maintain consistency with specifications
- Implement both frontend and backend components
- Ensure proper authentication and user isolation
- Follow established patterns in the codebase

## Specification Structure Template

### Feature Spec (`spec.md`)
```
# [Feature Name] Specification

## Overview
Brief description of the feature and its purpose.

## User Stories
### P1 (Critical)
- As a [user type], I want [feature] so that [benefit]

### P2 (Important)
- As a [user type], I want [feature] so that [benefit]

## Acceptance Criteria
- [Specific, testable criteria]

## Edge Cases
- [Consider error scenarios, boundary conditions]

## Clarifications
- [Record of questions and answers]
```

### Architecture Plan (`plan.md`)
```
# [Feature Name] Architecture Plan

## System Design
- [High-level architecture decisions]

## API Design
- [Endpoint definitions with request/response schemas]

## Database Design
- [Model definitions and relationships]

## Frontend Components
- [UI component structure]

## Security Considerations
- [Authentication, authorization, data validation]

## Trade-offs
- [Pros and cons of chosen approach]
```

### Implementation Tasks (`tasks.md`)
```
# [Feature Name] Implementation Tasks

## P1 Tasks
1. [Task description] - [Priority]
2. [Task description] - [Priority]

## Dependencies
- [List of task dependencies]

## Success Criteria
- [How to verify implementation is complete]
```

## Validation Checks

### Before Approving Specifications
- [ ] All user stories include clear acceptance criteria
- [ ] Specifications align with project constitution
- [ ] Edge cases and error scenarios are addressed
- [ ] Security and authentication requirements are specified
- [ ] Frontend and backend integration points are defined
- [ ] Database schema supports required functionality
- [ ] Performance considerations are addressed

### Before Approving Implementation Plan
- [ ] Architecture decisions include trade-off analysis
- [ ] API endpoints support required user stories
- [ ] Database schema supports all required operations
- [ ] Authentication flows are properly specified
- [ ] Error handling is planned for all scenarios
- [ ] Frontend components align with design system

## Agent Integration Guidelines

### For Spec Architect Agent
- Use this skill to create comprehensive feature specifications
- Ensure all specifications follow the template structure
- Validate specifications against project constitution
- Coordinate with other agents on cross-cutting concerns

### For Backend Engineer Agent
- Read specifications to understand API and database requirements
- Create implementation plans for backend components
- Generate tasks for API endpoints, database models, and business logic
- Ensure JWT authentication and user isolation are properly implemented

### For Frontend UI Agent
- Read specifications to understand UI requirements
- Create implementation plans for frontend components
- Generate tasks for UI components, pages, and client-side logic
- Ensure proper integration with backend APIs via JWT authentication

### For Auth Integrator Agent
- Read specifications to understand authentication requirements
- Create implementation plans for authentication flows
- Generate tasks for JWT handling, middleware, and security measures
- Ensure proper user isolation and data access controls

### For Architecture Planner Agent
- Use this skill to create high-level architecture plans
- Ensure consistency across frontend, backend, and database specifications
- Identify integration points and dependencies
- Validate architectural decisions against project constraints

## Output Formats

### Specification Output
- Markdown format following the template structure
- Saved to `specs/[feature]/spec.md`
- Includes all required sections (overview, user stories, acceptance criteria, etc.)

### Plan Output
- Markdown format following the architecture template
- Saved to `specs/[feature]/plan.md`
- Includes system design, API design, database design, and security considerations

### Tasks Output
- Markdown format with prioritized task list
- Saved to `specs/[feature]/tasks.md`
- Includes dependencies and success criteria

## Quality Standards

### Specification Quality
- Clear, unambiguous language
- Complete acceptance criteria for each user story
- Consideration of edge cases and error scenarios
- Alignment with project constitution and requirements

### Plan Quality
- Comprehensive architectural decisions with rationale
- Complete API and database specifications
- Proper security and authentication considerations
- Identification of potential risks and mitigation strategies

### Task Quality
- Actionable, specific task descriptions
- Clear dependencies and priorities
- Measurable success criteria
- Proper distribution across frontend and backend

## Integration with Project Constitution
- All specifications must align with the project constitution
- Changes to specifications require constitution review if they conflict
- Cross-reference constitution requirements in all specifications
- Ensure all features support the overall project vision

## Reusability Patterns
- Use consistent terminology across all specifications
- Create template snippets for common patterns
- Document reusable components and their specifications
- Maintain a library of validated architectural patterns

## Validation Workflow
1. Generate specification using appropriate template
2. Validate against quality standards checklist
3. Cross-reference with project constitution
4. Review for completeness and clarity
5. Approve for next stage in workflow