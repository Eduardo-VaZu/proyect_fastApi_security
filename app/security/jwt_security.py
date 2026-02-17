from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.env_config import env_config


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env_config.jwt_secret_key, algorithm=env_config.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """Create refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env_config.jwt_secret_key, algorithm=env_config.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str):
    """Decode access token"""
    try:
        return jwt.decode(
            token, env_config.jwt_secret_key, algorithms=[env_config.jwt_algorithm]
        )
    except JWTError:
        return None
