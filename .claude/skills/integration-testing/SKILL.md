# Integration Testing Skill for Full-Stack Todo App

## Overview
This skill enables agents (Integration Tester, Backend Engineer, Frontend UI, Spec Architect) to design, implement, and validate end-to-end tests across the full-stack Todo application. It focuses on creating modular, reusable, and spec-driven testing workflows, including frontend-backend integration, API validation, authentication flows, and multi-user task scenarios. All test cases align with project specs, validate feature correctness, handle error scenarios, and include performance, security, and accessibility checks.

## Purpose
- Enable comprehensive end-to-end testing for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all features work correctly across frontend, backend, and database layers
- Validate authentication and user isolation functionality
- Test error scenarios and edge cases
- Verify performance, security, and accessibility requirements
- Follow spec-driven testing methodology aligned with project specifications

## Testing Architecture Convention

### Directory Structure
```
/tests/
├── integration/
│   ├── __init__.py
│   ├── conftest.py             # Test configuration and fixtures
│   ├── test_auth.py            # Authentication integration tests
│   ├── test_tasks.py           # Task CRUD integration tests
│   ├── test_multi_user.py      # Multi-user isolation tests
│   └── test_api.py             # API endpoint integration tests
├── fixtures/
│   ├── __init__.py
│   ├── auth_fixtures.py        # Authentication test fixtures
│   ├── user_fixtures.py        # User test fixtures
│   └── task_fixtures.py        # Task test fixtures
├── utils/
│   ├── __init__.py
│   ├── test_client.py          # Test client utilities
│   ├── auth_helpers.py         # Authentication test helpers
│   └── data_generators.py      # Test data generation utilities
└── performance/
    ├── __init__.py
    └── load_tests.py           # Performance and load testing
```

### Test Categories
- **Authentication Tests**: User registration, login, token validation, logout
- **API Integration Tests**: End-to-end API endpoint validation
- **Multi-User Tests**: User isolation, data access control, permissions
- **Frontend-Backend Tests**: Full-stack integration validation
- **Performance Tests**: Load, stress, and performance validation
- **Security Tests**: Authentication bypass, data access, injection prevention
- **Error Handling Tests**: Validation, error responses, edge cases

## Development Workflow

### 1. Specification Reading
- Read feature specifications from `specs/[feature]/spec.md`
- Understand acceptance criteria for each user story
- Identify integration points between frontend and backend
- Note error scenarios and edge cases
- Extract performance and security requirements

### 2. Test Planning
- Create test plan in `specs/[feature]/plan.md`
- Design test scenarios for each feature
- Plan authentication and authorization tests
- Consider multi-user isolation scenarios
- Account for performance and security testing

### 3. Test Case Generation
- Break down testing into specific test cases
- Prioritize critical path functionality
- Plan for error scenarios and edge cases
- Consider cross-browser and accessibility testing
- Account for performance validation requirements

### 4. Implementation
- Follow testing best practices and patterns
- Implement modular, reusable test components
- Use proper test fixtures and data management
- Ensure comprehensive coverage of integration points
- Handle test data cleanup and isolation

## Testing Framework Patterns

### Pytest Configuration Pattern
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.db import get_session
from backend.models import User, Task, SQLModel

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create tables
SQLModel.metadata.create_all(bind=engine)

def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a database session"""
    def get_session_override():
        yield db_session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides[get_session] = get_session
```

### Authentication Test Pattern
```python
# tests/integration/test_auth.py
import pytest
from fastapi.testclient import TestClient
from backend.models import User
from tests.utils.auth_helpers import create_test_user, get_auth_token

def test_user_registration(client: TestClient):
    """Test user registration flow"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login(client: TestClient, db_session):
    """Test user login with valid credentials"""
    # Create a test user
    user = create_test_user(db_session, "login@example.com", "password123")

    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_endpoint_access(client: TestClient, db_session):
    """Test access to protected endpoints with valid token"""
    user = create_test_user(db_session, "protected@example.com", "password123")
    token = get_auth_token(client, "protected@example.com", "password123")

    response = client.get("/api/tasks", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
```

### Multi-User Isolation Test Pattern
```python
# tests/integration/test_multi_user.py
import pytest
from fastapi.testclient import TestClient
from backend.models import User, Task
from tests.utils.auth_helpers import create_test_user, get_auth_token

def test_user_task_isolation(client: TestClient, db_session):
    """Test that users can only access their own tasks"""
    # Create two users
    user1 = create_test_user(db_session, "user1@example.com", "password123")
    user2 = create_test_user(db_session, "user2@example.com", "password123")

    # User1 creates a task
    token1 = get_auth_token(client, "user1@example.com", "password123")
    task_response = client.post("/api/tasks", json={
        "title": "User 1 Task",
        "description": "This is user 1's task"
    }, headers={"Authorization": f"Bearer {token1}"})

    assert task_response.status_code == 200
    task_data = task_response.json()
    task_id = task_data["id"]

    # User2 should not be able to access User1's task
    token2 = get_auth_token(client, "user2@example.com", "password123")
    access_response = client.get(f"/api/tasks/{task_id}",
                                headers={"Authorization": f"Bearer {token2}"})

    # Should return 403 Forbidden or 404 Not Found
    assert access_response.status_code in [403, 404]

def test_user_task_list_isolation(client: TestClient, db_session):
    """Test that users only see their own tasks in lists"""
    # Create two users
    user1 = create_test_user(db_session, "list1@example.com", "password123")
    user2 = create_test_user(db_session, "list2@example.com", "password123")

    # Both users create tasks
    token1 = get_auth_token(client, "list1@example.com", "password123")
    token2 = get_auth_token(client, "list2@example.com", "password123")

    # User1 creates a task
    client.post("/api/tasks", json={
        "title": "User 1 Task",
        "description": "This is user 1's task"
    }, headers={"Authorization": f"Bearer {token1}"})

    # User2 creates a task
    client.post("/api/tasks", json={
        "title": "User 2 Task",
        "description": "This is user 2's task"
    }, headers={"Authorization": f"Bearer {token2}"})

    # User1 should only see their own task
    user1_tasks = client.get("/api/tasks",
                            headers={"Authorization": f"Bearer {token1}"})
    assert user1_tasks.status_code == 200
    user1_task_list = user1_tasks.json()
    assert len(user1_task_list) == 1
    assert user1_task_list[0]["title"] == "User 1 Task"

    # User2 should only see their own task
    user2_tasks = client.get("/api/tasks",
                            headers={"Authorization": f"Bearer {token2}"})
    assert user2_tasks.status_code == 200
    user2_task_list = user2_tasks.json()
    assert len(user2_task_list) == 1
    assert user2_task_list[0]["title"] == "User 2 Task"
```

### API Integration Test Pattern
```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from tests.utils.auth_helpers import get_auth_token

def test_task_crud_operations(client: TestClient, db_session):
    """Test complete task CRUD operations"""
    # Create user and get token
    from tests.utils.auth_helpers import create_test_user
    user = create_test_user(db_session, "crud@example.com", "password123")
    token = get_auth_token(client, "crud@example.com", "password123")

    # Create task
    create_response = client.post("/api/tasks", json={
        "title": "Test Task",
        "description": "Test task description",
        "completed": False
    }, headers={"Authorization": f"Bearer {token}"})

    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "Test task description"
    assert created_task["completed"] == False

    # Read task
    read_response = client.get(f"/api/tasks/{task_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert read_response.status_code == 200
    read_task = read_response.json()
    assert read_task["id"] == task_id
    assert read_task["title"] == "Test Task"

    # Update task
    update_response = client.put(f"/api/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    }, headers={"Authorization": f"Bearer {token}"})

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] == True

    # Delete task
    delete_response = client.delete(f"/api/tasks/{task_id}",
                                  headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 200

    # Verify task is deleted
    verify_response = client.get(f"/api/tasks/{task_id}",
                               headers={"Authorization": f"Bearer {token}"})
    assert verify_response.status_code in [404, 403]

def test_api_validation_errors(client: TestClient, db_session):
    """Test API validation error responses"""
    from tests.utils.auth_helpers import create_test_user
    user = create_test_user(db_session, "validation@example.com", "password123")
    token = get_auth_token(client, "validation@example.com", "password123")

    # Test creating task with empty title (should fail validation)
    response = client.post("/api/tasks", json={
        "title": "",  # Empty title should fail validation
        "description": "Valid description"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 422  # Validation error
    error_data = response.json()
    assert "detail" in error_data

    # Test creating task with title that's too long
    long_title = "x" * 300  # Exceeds max length of 255
    response = client.post("/api/tasks", json={
        "title": long_title,
        "description": "Valid description"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 422  # Validation error
```

## Testing Best Practices

### Test Data Management
- Use fixtures for consistent test data setup
- Implement proper test data cleanup
- Isolate test data between test runs
- Use factory patterns for test data generation
- Avoid shared state between tests

### Test Organization
- Group related tests in logical modules
- Use descriptive test names following naming conventions
- Separate unit, integration, and end-to-end tests
- Organize tests by feature or component
- Use parametrized tests for multiple scenarios

### Error Scenario Testing
- Test invalid input and edge cases
- Validate proper error responses and status codes
- Test authentication and authorization failures
- Verify proper error handling and logging
- Test resource not found scenarios

### Performance Testing
- Measure response times for critical operations
- Test concurrent user scenarios
- Validate database query performance
- Test API rate limiting
- Monitor resource usage during tests

## Security Testing Patterns

### Authentication Bypass Testing
```python
def test_unauthorized_access_to_protected_endpoints(client: TestClient):
    """Test that protected endpoints require authentication"""
    # Try to access protected endpoint without token
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized

    # Try with invalid token
    response = client.get("/api/tasks", headers={
        "Authorization": "Bearer invalid_token"
    })
    assert response.status_code == 401  # Unauthorized
```

### Data Access Control Testing
```python
def test_cross_user_data_access(client: TestClient, db_session):
    """Test that users cannot access other users' data"""
    # Create two users
    user1 = create_test_user(db_session, "attacker@example.com", "password123")
    user2 = create_test_user(db_session, "victim@example.com", "password123")

    # Victim creates a task
    victim_token = get_auth_token(client, "victim@example.com", "password123")
    task_response = client.post("/api/tasks", json={
        "title": "Victim's Task",
        "description": "This belongs to victim"
    }, headers={"Authorization": f"Bearer {victim_token}"})

    victim_task_id = task_response.json()["id"]

    # Attacker tries to access victim's task using direct ID access
    attacker_token = get_auth_token(client, "attacker@example.com", "password123")
    access_response = client.get(f"/api/tasks/{victim_task_id}",
                               headers={"Authorization": f"Bearer {attacker_token}"})

    # Should not be able to access
    assert access_response.status_code in [403, 404]
```

## Frontend-Backend Integration Testing

### End-to-End Test Pattern
```python
# Using Playwright or similar for frontend testing
import pytest
from playwright.sync_api import Page, expect

def test_complete_task_workflow(page: Page):
    """Test complete task management workflow from frontend"""
    # Navigate to login page
    page.goto("http://localhost:3000/login")

    # Fill login form
    page.get_by_label("Email").fill("test@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Login").click()

    # Wait for redirect to dashboard
    expect(page).to_have_url("http://localhost:3000/dashboard")

    # Create a new task
    page.get_by_placeholder("Add a new task...").fill("Test task from frontend")
    page.get_by_role("button", name="Add Task").click()

    # Verify task appears in the list
    expect(page.get_by_text("Test task from frontend")).to_be_visible()

    # Mark task as complete
    page.get_by_label("Complete task").click()

    # Verify task is marked as complete
    completed_task = page.get_by_text("Test task from frontend")
    expect(completed_task).to_have_css("text-decoration", "line-through")

    # Delete the task
    page.get_by_role("button", name="Delete").click()

    # Verify task is removed
    expect(page.get_by_text("Test task from frontend")).not_to_be_visible()
```

## Validation Checks

### Before Creating Test Cases
- [ ] Feature specifications and acceptance criteria are clear
- [ ] Integration points between components are identified
- [ ] Error scenarios and edge cases are documented
- [ ] Performance requirements are specified
- [ ] Security and privacy requirements are noted

### Before Implementing Integration Tests
- [ ] Test environment setup is properly configured
- [ ] Database isolation strategy is defined
- [ ] Authentication testing approach is planned
- [ ] Multi-user scenario testing is considered
- [ ] Performance testing requirements are identified

### Before Running Tests
- [ ] Test data is properly isolated and clean
- [ ] Dependencies are properly mocked or configured
- [ ] Test environment matches production as closely as possible
- [ ] Security testing is included in the test suite
- [ ] Performance benchmarks are established

## Agent Integration Guidelines

### For Integration Tester Agent
- Use this skill to design comprehensive end-to-end test scenarios
- Implement modular, reusable test components
- Validate multi-user isolation and security
- Test error scenarios and edge cases
- Ensure comprehensive feature coverage

### For Backend Engineer Agent
- Create API integration tests for new endpoints
- Validate authentication and authorization flows
- Test database interactions and user isolation
- Implement performance validation tests
- Handle error scenario testing

### For Frontend UI Agent
- Implement frontend-backend integration tests
- Test user interface workflows end-to-end
- Validate authentication flows from UI perspective
- Test responsive design and accessibility
- Ensure proper error handling in UI

### For Spec Architect Agent
- Define testing requirements in specifications
- Plan integration test scenarios for features
- Consider security and performance testing needs
- Specify error handling and validation requirements
- Account for cross-component testing needs

## Quality Standards

### Test Quality
- Follow consistent naming conventions for tests
- Use descriptive test names that explain the scenario
- Implement proper test data management
- Ensure tests are independent and isolated
- Write maintainable and readable test code

### Coverage Quality
- Achieve comprehensive feature coverage
- Test both happy path and error scenarios
- Include security and performance tests
- Validate multi-user isolation
- Test edge cases and boundary conditions

### Performance Quality
- Measure and monitor test execution times
- Optimize slow-running tests
- Implement parallel test execution where possible
- Monitor resource usage during testing
- Set performance benchmarks and alerts

## Integration with Spec-Driven Development

### Reading Specifications
- Parse feature specs to understand acceptance criteria
- Identify integration points between components
- Note error scenarios and edge cases
- Extract performance and security requirements
- Consider multi-user scenarios and isolation needs

### Generating Test Plans
- Create detailed test scenarios based on specs
- Design integration test flows for each feature
- Plan authentication and authorization validation
- Consider performance and security testing
- Account for cross-component dependencies

### Test Case Generation
- Break down feature requirements into specific test cases
- Prioritize critical functionality tests
- Plan for error scenario validation
- Account for security and performance validation
- Consider user experience validation

## Output Formats

### Test Case Output
- Pytest test functions with proper assertions
- Test data fixtures and setup functions
- Parametrized test scenarios
- Test configuration and utility functions

### Test Report Output
- Comprehensive test execution reports
- Coverage reports for integration points
- Performance benchmark results
- Security validation reports

### Test Data Output
- Test data generation utilities
- Database fixture patterns
- Authentication test helpers
- Mock data and response patterns

## Reusability Patterns

### Common Test Utilities
- Authentication test helpers
- Database fixture generators
- API response validators
- Test data factories

### Test Configuration Patterns
- Environment setup and teardown
- Database connection management
- Authentication token management
- Test isolation utilities

### Assertion and Validation Patterns
- Standardized response validation
- Error message validation
- Status code verification
- Data integrity checks

## Testing Guidelines

### Unit Tests
- Test individual functions and utilities
- Mock external dependencies
- Validate input/output behavior
- Test error handling paths

### Integration Tests
- Test component interactions
- Validate API endpoints with real database
- Test authentication and authorization flows
- Verify multi-user isolation

### End-to-End Tests
- Test complete user workflows
- Validate frontend-backend integration
- Test cross-component functionality
- Verify user experience scenarios

### Performance Tests
- Measure response times for critical operations
- Test concurrent user scenarios
- Validate database query performance
- Monitor resource usage under load

### Security Tests
- Test authentication bypass scenarios
- Validate data access controls
- Test injection prevention
- Verify proper error handling