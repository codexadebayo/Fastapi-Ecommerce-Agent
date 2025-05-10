from config.config import get_config
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

config = get_config()


engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
    pool_pre_ping=True,  # Add pool_pre_ping for async
)

# Asynchronous Session
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)  # expire_on_commit=False is good for async

Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous dependency injection for database sessions.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()  # Ensure session is closed





