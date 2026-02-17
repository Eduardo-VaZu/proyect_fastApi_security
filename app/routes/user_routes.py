from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user_schemas import ResponseUserSchemas, RequestUserSchemas
from app.services.user_service import UserService
from app.dependecies.dependecies_config import get_user_service
from app.dependecies.dependecies_oauth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[ResponseUserSchemas])
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Get all users"""
    if current_user.is_active:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await user_service.find_all()


@router.get("/{user_id}", response_model=ResponseUserSchemas)
async def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Get user by ID"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return await user_service.find_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/search/{username}", response_model=List[ResponseUserSchemas])
async def search_users(
    username: str,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Search users by username"""
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await user_service.search(username)


@router.get("/email/{email}", response_model=ResponseUserSchemas)
async def get_user_by_email(
    email: str,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Get user by email"""
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return await user_service.find_by_email(email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=ResponseUserSchemas, status_code=201)
async def create_user(
    user: RequestUserSchemas,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Create a new user"""
    if current_user.is_active:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return await user_service.create(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=ResponseUserSchemas)
async def update_user(
    user_id: int,
    user: RequestUserSchemas,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Update a user"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return await user_service.update(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: ResponseUserSchemas = Depends(get_current_user),
):
    """Delete a user"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        await user_service.delete(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
