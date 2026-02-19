from app.security.jwt_security import (
    create_access_token,
    decode_access_token,
    create_refresh_token,
)
from datetime import timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.config.env_config import env_config
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import RequestLoginSchema, ResponseLoginSchema
from app.services.auth_service import AuthService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServiceImpl(AuthService):
    """Implementation service of authentication"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def login(self, data: RequestLoginSchema) -> ResponseLoginSchema:
        """Login user"""
        user = await self.user_repository.find_by_email(data.username)

        if not user or not pwd_context.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=env_config.jwt_access_token_expire_minutes
        )

        refresh_token_expires = timedelta(
            minutes=env_config.jwt_refresh_token_expire_minutes
        )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "username": user.username,
                "is_active": user.is_active,
            },
            expires_delta=access_token_expires,
        )

        refresh_token = create_refresh_token(
            data={"sub": user.email, "username": user.username},
            expires_delta=refresh_token_expires,
        )

        return ResponseLoginSchema(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    async def refresh_token(self, token: str) -> ResponseLoginSchema:
        """Refresh token"""
        is_valid_token = decode_access_token(token)
        if not is_valid_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=env_config.jwt_access_token_expire_minutes
        )
        access_token = create_access_token(
            data={"sub": is_valid_token["sub"], "username": is_valid_token["username"]},
            expires_delta=access_token_expires,
        )

        return ResponseLoginSchema(access_token=access_token, token_type="bearer")

    async def logout(self, token: str) -> None:
        """Close session of a user"""
        is_valid_token = decode_access_token(token)
        if not is_valid_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"message": "Logged out successfully"}
