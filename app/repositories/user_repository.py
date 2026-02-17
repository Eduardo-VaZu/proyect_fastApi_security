from typing import Optional
from app.entities.user_entities import UserEntities
from abc import ABC, abstractmethod


class UserRepository(ABC):
    """Abstract interface for the user repository"""

    @abstractmethod
    async def save(self, user: UserEntities) -> UserEntities:
        """Save a new user"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[UserEntities]:
        """Find user by ID"""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserEntities]:
        """Find user by email"""
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[UserEntities]:
        """Find user by username"""
        pass

    @abstractmethod
    async def search_by_username(self, username: str) -> list[UserEntities]:
        """Search users by username partial match"""
        pass

    @abstractmethod
    async def find_all(self) -> list[UserEntities]:
        """Get all users"""
        pass

    @abstractmethod
    async def update(self, user: UserEntities) -> UserEntities:
        """Update existing user"""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Delete user by ID"""
        pass
