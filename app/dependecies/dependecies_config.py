from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database_config import AsyncSessionLocal
from app.repositories.impl.user_repository_impl import UserRepositoryImpl
from app.services.impl.user_service_impl import UserServiceImpl
from app.services.impl.auth_service_impl import AuthServiceImpl


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Proporcionar sesión de base de datos con gestión de transacciones"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def get_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryImpl:
    """Proporcionar repositorio con la sesión de base de datos inyectada"""
    return UserRepositoryImpl(db)


async def get_user_service(
    repository: UserRepositoryImpl = Depends(get_repository),
) -> UserServiceImpl:
    """Proporcionar servicio de usuario con el repositorio inyectado"""
    return UserServiceImpl(repository)


async def get_auth_service(
    repository: UserRepositoryImpl = Depends(get_repository),
) -> AuthServiceImpl:
    """Proporcionar servicio de autenticación con repositorio inyectado"""
    return AuthServiceImpl(repository)
