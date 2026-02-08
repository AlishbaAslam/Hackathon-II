"""
FastAPI application entry point.
"""
from fastapi import FastAPI, Request, HTTPException as FastAPIHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from src.config import settings
from src.core.database import create_tables
from src.routers import auth, tasks, chat, events
from src.core.exceptions import UnauthorizedException, ForbiddenException, NotFoundException, ConflictException

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    await create_tables()
    yield
    # Shutdown: Cleanup (if needed)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)
app.include_router(events.router)


# Exception handlers
@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ],
            "status_code": 422
        }
    )


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    """Handle FastAPI HTTP exceptions with consistent error format."""
    # For 401, 403, 404, 409 errors, return the expected format
    if exc.status_code in [401, 403, 404, 409]:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail if hasattr(exc, 'detail') and exc.detail else "An error occurred",
                "status_code": exc.status_code
            }
        )
    # For other HTTP exceptions, use default behavior
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail if hasattr(exc, 'detail') and exc.detail else "An error occurred",
            "status_code": exc.status_code
        }
    )


# Generic exception handler for internal server errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the error internally for debugging
    import logging
    logging.error(f"Internal server error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo Backend API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
