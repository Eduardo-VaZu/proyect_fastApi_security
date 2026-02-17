from fastapi.security import OAuth2PasswordRequestForm
from app.security.cookie_security import create_access_cookie, create_refresh_cookie
from app.schemas.auth_schemas import ResponseLoginSchema, RequestLoginSchema
from app.services.auth_service import AuthService
from app.dependecies.dependecies_config import get_auth_service
from fastapi import APIRouter, Depends, Response, Request

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=ResponseLoginSchema)
async def login(
    response: Response,
    data: RequestLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    user_login = await auth_service.login(data)
    create_access_cookie(response, user_login.access_token)
    create_refresh_cookie(response, user_login.refresh_token)

    return user_login


@router.post("/login/form", response_model=ResponseLoginSchema)
async def login_form(
    response: Response,
    data_form: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await login(
        response=response,
        data=RequestLoginSchema(
            username=data_form.username, password=data_form.password
        ),
        auth_service=auth_service,
    )


@router.post("/logout", status_code=200)
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = request.cookies.get("access_token")
    if token:
        await auth_service.logout(token.replace("Bearer ", ""))

    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
