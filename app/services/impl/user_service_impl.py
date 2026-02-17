from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import RequestUserSchemas, ResponseUserSchemas
from app.services.user_service import UserService
from app.entities.user_entities import UserEntities
from app.security.password_security import hash_password


class UserServiceImpl(UserService):
    """Implementation of the user service"""

    def __init__(self, user_repository: UserRepository):
        """Initialize the user service"""
        self.user_repository = user_repository

    async def create(self, user: RequestUserSchemas) -> ResponseUserSchemas:
        """Create a new user"""
        # Validate email is unique
        existing_email = await self.user_repository.find_by_email(user.email)
        if existing_email:
            raise ValueError(f"Email '{user.email}' is already registered")

        # Validate username is unique
        existing_username = await self.user_repository.find_by_username(user.username)
        if existing_username:
            raise ValueError(f"Username '{user.username}' is already taken")

        # Convert schema to entity and hash password
        user_entity = UserEntities(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            is_active=True,
        )

        # Save to database
        created_user = await self.user_repository.save(user_entity)

        # Convert entity back to response schema
        return ResponseUserSchemas.model_validate(created_user)

    async def find_by_id(self, user_id: int) -> ResponseUserSchemas:
        """Find user by ID"""
        found_user = await self.user_repository.find_by_id(user_id)
        if found_user is None:
            raise ValueError(f"User with ID {user_id} not found")
        return ResponseUserSchemas.model_validate(found_user)

    async def find_by_email(self, email: str) -> ResponseUserSchemas:
        """Find user by email"""
        found_user = await self.user_repository.find_by_email(email)
        if found_user is None:
            raise ValueError(f"User with email {email} not found")
        return ResponseUserSchemas.model_validate(found_user)

    async def find_all(self) -> list[ResponseUserSchemas]:
        """Get all users"""
        found_users = await self.user_repository.find_all()
        return [ResponseUserSchemas.model_validate(user) for user in found_users]

    async def search(self, username: str) -> list[ResponseUserSchemas]:
        """Search users by username partial match"""
        found_users = await self.user_repository.search_by_username(username)
        return [ResponseUserSchemas.model_validate(user) for user in found_users]

    async def update(
        self, user_id: int, user: RequestUserSchemas
    ) -> ResponseUserSchemas:
        """Update existing user"""
        # Find user by ID
        existing_user = await self.user_repository.find_by_id(user_id)
        if existing_user is None:
            raise ValueError(f"User with ID {user_id} not found")

        # Update fields
        existing_user.username = user.username
        existing_user.email = user.email
        existing_user.password = pwd_context.hash(user.password)

        updated_user = await self.user_repository.update(existing_user)
        return ResponseUserSchemas.model_validate(updated_user)

    async def delete(self, user_id: int) -> None:
        """Delete user by ID"""
        await self.user_repository.delete(user_id)
