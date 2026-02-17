from app.repositories.user_repository import UserRepository
from app.entities.user_entities import UserEntities
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Optional


class UserRepositoryImpl(UserRepository):
    """Implementation of the user repository with dependency injection pattern"""

    def __init__(self, db: AsyncSession):
        """Initialize the repository with a database session"""
        self._db = db

    async def save(self, user: UserEntities) -> UserEntities:
        """Save a new user to the database"""
        self._db.add(user)
        await self._db.flush()
        await self._db.refresh(user)
        return user

    async def find_by_id(self, user_id: int) -> Optional[UserEntities]:
        """Find user by ID"""
        result = await self._db.execute(
            select(UserEntities).where(UserEntities.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> Optional[UserEntities]:
        """Find user by email"""
        result = await self._db.execute(
            select(UserEntities).where(UserEntities.email == email)
        )
        return result.scalar_one_or_none()

    async def find_by_username(self, username: str) -> Optional[UserEntities]:
        """Find user by username"""
        result = await self._db.execute(
            select(UserEntities).where(UserEntities.username == username)
        )
        return result.scalar_one_or_none()

    async def search_by_username(self, username: str) -> list[UserEntities]:
        """Search users by username partial match"""
        result = await self._db.execute(
            select(UserEntities).where(UserEntities.username.ilike(f"%{username}%"))
        )
        return list(result.scalars().all())

    async def find_all(self) -> list[UserEntities]:
        """Get all users ordered by ID"""
        result = await self._db.execute(
            select(UserEntities).order_by(UserEntities.id.asc())
        )
        return list(result.scalars().all())

    async def update(self, user: UserEntities) -> UserEntities:
        """Update existing user"""
        await self._db.merge(user)
        await self._db.flush()
        await self._db.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        """Delete user by ID"""
        await self._db.execute(delete(UserEntities).where(UserEntities.id == user_id))
        await self._db.flush()
