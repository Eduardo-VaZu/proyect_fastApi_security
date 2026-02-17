from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.user_schemas import RequestUserSchemas, ResponseUserSchemas


class UserService(ABC):
    """Abstract interface for the user service"""

    @abstractmethod
    async def create(self, user: RequestUserSchemas) -> ResponseUserSchemas:
        """Create a new user"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: int) -> ResponseUserSchemas:
        """Find user by ID"""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> ResponseUserSchemas:
        """Find user by email"""
        pass

    @abstractmethod
    async def search(self, username: str) -> list[ResponseUserSchemas]:
        """Search users by username partial match"""
        pass

    @abstractmethod
    async def find_all(self) -> list[ResponseUserSchemas]:
        """Get all users"""
        pass

    @abstractmethod
    async def update(
        self, user_id: int, user: RequestUserSchemas
    ) -> ResponseUserSchemas:
        """Update existing user"""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Delete user by ID"""
        pass
