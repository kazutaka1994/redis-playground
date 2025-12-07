from fastapi import APIRouter, Depends, HTTPException, Query

from ..models import User
from ..services.user_service import UserService
from .dependencies import get_user_service

router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    use_cache: bool = Query(True, description="Use cache"),
    service: UserService = Depends(get_user_service),
):
    user = service.get_user_by_id(user_id, use_cache=use_cache)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/email/{email}", response_model=User)
async def get_user_by_email(
    email: str,
    use_cache: bool = Query(True, description="Use cache"),
    service: UserService = Depends(get_user_service),
):
    user = service.get_user_by_email(email, use_cache=use_cache)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/cache/users/{user_id}")
async def invalidate_user_cache(user_id: int, service: UserService = Depends(get_user_service)):
    service.invalidate_cache(user_id)
    return {"message": f"Cache invalidated for user {user_id}"}
