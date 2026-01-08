# Authentication Integration Skill (Better Auth + JWT) for Full-Stack Todo App

## Overview
This skill enables agents (Auth Integrator, Backend Engineer, Spec Architect) to implement, manage, and validate authentication and authorization workflows using Better Auth and JWT. It focuses on creating modular, reusable, and spec-driven auth logic, including user registration, login, token issuance and verification, role-based access control, and secure API access. All auth components align with project specs, backend models, and frontend integration patterns, following security best practices.

## Purpose
- Enable rapid authentication and authorization implementation for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all auth components follow spec-driven development methodology
- Maintain consistency in Better Auth + JWT patterns across the codebase
- Implement secure user registration, login, and token management
- Ensure proper user isolation and data access controls
- Follow security best practices for authentication and authorization

## Authentication Architecture Convention

### Directory Structure
```
/backend/
├── auth.py                 # JWT authentication middleware and utilities
├── models.py               # User model with authentication fields
├── api/v1/auth.py          # Authentication endpoints
├── schemas/auth.py         # Authentication request/response schemas
├── utils/security.py       # Security utilities (password hashing, token generation)
└── config.py               # Authentication configuration settings

/frontend/
├── components/
│   └── auth/               # Authentication UI components
├── lib/
│   └── auth.js             # Authentication utilities and hooks
├── pages/
│   ├── login.js            # Login page
│   ├── signup.js           # Registration page
│   └── profile.js          # User profile page
└── middleware.js           # Authentication middleware (if needed)
```

### Token Flow Architecture
```
User Registration → Create User → Store Hashed Password
User Login → Validate Credentials → Issue JWT Token
API Request → Verify JWT Token → Extract User ID → Validate Permissions
```

## Development Workflow

### 1. Specification Reading
- Read authentication specifications from `specs/[feature]/spec.md`
- Understand user registration/login requirements
- Identify token management needs
- Note role-based access requirements
- Extract security and privacy requirements

### 2. Authentication Design Planning
- Create auth architecture plan in `specs/[feature]/plan.md`
- Design token issuance and validation flows
- Plan user registration and login workflows
- Define role-based access control structure
- Consider session management and security measures

### 3. Task Generation
- Break down auth implementation into specific tasks
- Prioritize user model creation before authentication endpoints
- Plan token management and validation
- Account for frontend integration requirements
- Consider testing and validation of auth flows

### 4. Implementation
- Follow Better Auth + JWT best practices
- Implement secure password hashing
- Create proper token validation middleware
- Ensure user isolation and data access controls
- Handle authentication errors gracefully

## Better Auth + JWT Implementation Patterns

### User Model Pattern
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
import bcrypt

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    role: str = Field(default="user", max_length=20)  # user, admin, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
```

### JWT Token Generation Pattern
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a token and return the payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None
```

### Authentication Middleware Pattern
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Get current user ID from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user is active
    # This would require a database session
    # user = session.get(User, user_id)
    # if not user or not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User account is inactive",
    #     )

    return user_id

async def get_current_active_user(current_user_id: int = Depends(get_current_user)) -> int:
    """Get current active user with additional checks"""
    # Additional checks can be added here
    return current_user_id
```

### Role-Based Access Control Pattern
```python
from fastapi import Depends, HTTPException, status
from typing import List

def require_role(required_roles: List[str]):
    """Create a dependency that checks user roles"""
    async def role_checker(current_user_id: int = Depends(get_current_user)) -> int:
        # In a real implementation, this would fetch the user from the database
        # to check their role
        # user = session.get(User, current_user_id)
        # if user.role not in required_roles:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Insufficient permissions"
        #     )
        return current_user_id
    return role_checker

# Usage in endpoints
@router.get("/admin/users", dependencies=[Depends(require_role(["admin"]))])
async def get_all_users():
    """Only admin users can access this endpoint"""
    pass
```

### Authentication API Endpoints Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_session
from backend.models import User
from backend.schemas.auth import UserCreate, UserLogin, Token
from backend.auth import create_access_token
from backend.utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=Token)
async def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    hashed_password = User.hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token
    access_token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(
    user_data: UserLogin,
    session: Session = Depends(get_session)
):
    """Authenticate user and return access token"""
    # Find user by email
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if not user or not user.verify_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
```

## Security Best Practices

### Password Security
- Use bcrypt for password hashing with appropriate cost factor
- Enforce strong password requirements (length, complexity)
- Never log or store plaintext passwords
- Implement password reset functionality
- Use secure random generators for salt values

### Token Security
- Use strong, randomly generated secret keys
- Set appropriate token expiration times
- Implement token refresh mechanisms
- Use HTTPS in production for token transmission
- Consider token blacklisting for logout functionality

### Session Management
- Implement secure session storage
- Use secure, HTTP-only cookies for token storage
- Implement proper logout functionality
- Consider session timeout and re-authentication
- Monitor for suspicious authentication activities

### Rate Limiting
- Implement rate limiting for authentication endpoints
- Prevent brute force attacks
- Use CAPTCHA for suspicious activities
- Monitor and alert on authentication failures
- Consider temporary account lockout after failed attempts

## User Isolation Patterns

### Data Access Control
- Always verify user_id matches authenticated user
- Use middleware to extract and validate user context
- Implement row-level security where appropriate
- Validate user permissions for each operation
- Prevent user enumeration through timing attacks

### Multi-Tenant Security
- Ensure users can only access their own data
- Implement proper foreign key relationships
- Use parameterized queries to prevent injection
- Validate user context in all data access operations
- Implement proper error messages that don't leak information

## Frontend Integration Patterns

### Token Storage
- Store tokens securely in memory or HTTP-only cookies
- Implement automatic token refresh
- Handle token expiration gracefully
- Clear tokens on logout
- Prevent XSS by avoiding localStorage for sensitive tokens

### Authentication State Management
```javascript
// Example React context for authentication
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on app load
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      // Validate token with backend
      validateToken(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      if (response.ok) {
        setToken(data.access_token);
        localStorage.setItem('auth_token', data.access_token);
        setUser(data.user);
      }
      return response.ok;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

## Validation Checks

### Before Implementing Authentication
- [ ] Authentication requirements are clearly specified
- [ ] User registration/login workflows are defined
- [ ] Token management requirements are identified
- [ ] Role-based access requirements are specified
- [ ] Security and privacy requirements are addressed
- [ ] Frontend integration requirements are noted

### Before Creating User Models
- [ ] User data requirements are complete
- [ ] Password security requirements are defined
- [ ] User verification and activation flows are planned
- [ ] Role and permission structures are specified
- [ ] Data validation rules are established

### Before Adding Token Management
- [ ] JWT configuration is properly planned
- [ ] Secret key management is addressed
- [ ] Token expiration policies are defined
- [ ] Token refresh mechanisms are planned
- [ ] Logout and token invalidation are considered

## Agent Integration Guidelines

### For Auth Integrator Agent
- Use this skill to implement comprehensive authentication flows
- Create JWT token generation and validation utilities
- Implement role-based access control
- Ensure proper user isolation and security
- Handle authentication errors gracefully

### For Backend Engineer Agent
- Integrate authentication with API endpoints
- Implement secure password hashing
- Create proper authentication middleware
- Ensure user isolation in data access
- Follow security best practices for token management

### For Spec Architect Agent
- Define authentication and authorization requirements
- Plan token management and session strategies
- Specify role-based access control requirements
- Consider security and privacy implications
- Plan for frontend authentication integration

## Quality Standards

### Security Quality
- Implement strong password hashing with bcrypt
- Use secure random generators for tokens
- Follow OWASP authentication security guidelines
- Implement proper input validation
- Use HTTPS for all authentication flows

### Code Quality
- Follow consistent naming conventions
- Use type hints for all function signatures
- Implement proper error handling
- Include comprehensive documentation
- Write maintainable and testable code

### Performance Quality
- Optimize token validation performance
- Implement efficient user lookup queries
- Use connection pooling for database operations
- Cache frequently accessed authentication data
- Minimize database queries in authentication flows

## Integration with Spec-Driven Development

### Reading Specifications
- Parse auth specs to understand registration/login requirements
- Identify token management and security requirements
- Note role-based access and user isolation needs
- Extract frontend integration requirements
- Consider multi-tenant security requirements

### Generating Implementation Plans
- Create detailed authentication architecture plans
- Design token issuance and validation flows
- Plan user registration and login workflows
- Consider session management and security measures
- Account for frontend integration patterns

### Task Generation
- Break down authentication implementation into specific tasks
- Prioritize critical security components
- Plan for testing and validation of auth flows
- Account for error handling and edge cases
- Consider deployment and monitoring requirements

## Output Formats

### Authentication Model Output
- SQLModel classes with proper authentication fields
- Password hashing and verification methods
- User validation and security constraints
- Role and permission definitions

### Token Management Output
- JWT token generation and validation utilities
- Authentication middleware functions
- Token refresh and expiration handling
- Secure token storage patterns

### API Endpoint Output
- Authentication endpoint implementations
- Request/response schemas for auth flows
- Error handling and validation patterns
- Security headers and protections

## Reusability Patterns

### Common Authentication Utilities
- Password hashing and verification functions
- Token generation and validation utilities
- User identification and authorization functions
- Secure session management helpers

### Middleware Patterns
- Authentication verification middleware
- Role-based access control middleware
- User isolation validation middleware
- Token refresh and validation middleware

### Error Handling Patterns
- Standardized authentication error responses
- User-friendly error messages
- Security-aware error handling
- Audit trail for authentication failures

## Testing Guidelines

### Unit Tests
- Test password hashing and verification
- Validate token generation and validation
- Test role-based access control logic
- Verify user isolation mechanisms
- Test error handling paths

### Integration Tests
- Test complete authentication flows
- Verify token-based API access
- Test user isolation between different users
- Validate security measures and protections
- Test authentication with real database operations