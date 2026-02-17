from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from fastapi import Depends, HTTPException
from app.services.impl.user_service_impl import UserServiceImpl
from app.dependecies.dependecies_config import get_user_service
from app.security.jwt_security import decode_access_token
from app.schemas.user_schemas import ResponseUserSchemas

# oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login/form")
bearer_schema = HTTPBearer()


async def get_current_user(
    user_service: UserServiceImpl = Depends(get_user_service),
    # token: str = Depends(oauth2_schema),
    creds: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> ResponseUserSchemas:
    try:
        token = creds.credentials
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_email = payload["sub"]
        user = await user_service.find_by_email(user_email)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
