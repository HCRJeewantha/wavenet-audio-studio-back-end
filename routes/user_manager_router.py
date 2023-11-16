from typing import Optional
from fastapi import APIRouter, Depends, Body, Query, UploadFile, HTTPException, File
from controllers.user_manager_controller import create_user
from request.user_requests import CreateUserRequest

router = APIRouter(
    prefix="/user-manager",
    tags=["User Manager"],
)

@router.post("/create-account")
async def register(request: CreateUserRequest):
    return await create_user(request)

