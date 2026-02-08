"""
Application configuration loaded from environment variables.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

    # JWT Configuration - Use same secret for both to ensure compatibility
    SECRET_KEY: str = os.getenv("SECRET_KEY", os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-this-in-production"))
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", os.getenv("SECRET_KEY", "fallback-secret-key-change-this"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:41397",
        "http://127.0.0.1:41397",
        ]

    # Application Settings
    API_TITLE: str = os.getenv("API_TITLE", "Todo Backend API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Kafka Configuration for Event-Driven Architecture
    KAFKA_BROKERS: str = os.getenv("KAFKA_BROKERS", "localhost:9092")
    KAFKA_TASK_EVENTS_TOPIC: str = os.getenv("KAFKA_TASK_EVENTS_TOPIC", "task-events")
    KAFKA_REMINDERS_TOPIC: str = os.getenv("KAFKA_REMINDERS_TOPIC", "reminders")
    KAFKA_TASK_UPDATES_TOPIC: str = os.getenv("KAFKA_TASK_UPDATES_TOPIC", "task-updates")

    # Dapr Configuration
    DAPR_HTTP_ENDPOINT: str = os.getenv("DAPR_HTTP_ENDPOINT", "http://localhost:3500")
    DAPR_GRPC_ENDPOINT: str = os.getenv("DAPR_GRPC_ENDPOINT", "grpc://localhost:50001")
    DAPR_API_TOKEN: str = os.getenv("DAPR_API_TOKEN", "")

# Global settings instance
settings = Settings()
