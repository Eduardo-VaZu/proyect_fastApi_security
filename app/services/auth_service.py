from abc import ABC, abstractmethod
from app.schemas.auth_schemas import RequestLoginSchema, ResponseLoginSchema


class AuthService(ABC):
    """Interfaz para el servicio de autenticación"""

    @abstractmethod
    async def login(self, data: RequestLoginSchema) -> ResponseLoginSchema:
        """Autenticar usuario y generar token"""
        pass

    @abstractmethod
    async def refresh_token(self, token: str) -> ResponseLoginSchema:
        """Refrescar token"""
        pass

    @abstractmethod
    async def logout(self, token: str) -> None:
        """Cerrar sesión de un usuario"""
        pass
