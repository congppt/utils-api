import os

from database.manager import DatabaseSessionManager
from database.models.organization import *

__DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///utildb")

DATABASE = DatabaseSessionManager(
    url=__DB_URL,
    pool_size=5,
    max_overflow=10,  # max_overflow + pool_size = max size = 15
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Phát hiện và loại bỏ kết nối chết
)

async def aget_db():
    """Retrieve a database session"""
    async with DATABASE.aget_session() as session:
        yield session