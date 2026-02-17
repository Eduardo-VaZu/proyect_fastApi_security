from fastapi import Response


def create_access_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
    )


def create_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
    )
