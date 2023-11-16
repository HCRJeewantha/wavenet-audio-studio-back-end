from typing import Optional
from fastapi import APIRouter, Depends, Body, Query, UploadFile, HTTPException, File
from controllers.auth_controller import login_user
from request.user_requests import LoginUserRequest

router = APIRouter(
    prefix="/authentication",
    tags=["Auth Manager"],
)

@router.post("/login")
async def login(request: LoginUserRequest):
    return await login_user(request)

