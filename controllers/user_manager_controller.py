from services.jwt_auth import create_token
from models.sqlite_models import User
from request.user_requests import CreateUserRequest
from sqlalchemy.orm import Session
from database.sqlite_connection import get_db
from fastapi import HTTPException
from services.hash_password import  verify_password
from fastapi.responses import JSONResponse
import os
import uuid
from services.hash_password import hash_password
from sqlalchemy.exc import IntegrityError


otp_valid = os.getenv('OTP_VALID')
db: Session = next(get_db())

async def create_user(request: CreateUserRequest):
    try:
        # with db.begin():
            user = User(
                username=request.username,
                first_name=request.first_name,
                last_name=request.last_name,
                primary_email=request.primary_email,
                password=hash_password(request.password),
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            return {
                    "status": True,
                    "message": "User has been created successful",
                    "result": user
                }
    
    except IntegrityError as e:
        error_info = str(e.orig)
        if "already exists" in error_info:
            # Handle the duplicate key violation error
            raise HTTPException(
                status_code=422,
                detail={
                    "status": False,
                    "result": "Primary data already exist"
                }
            )
        # HTTP 500 Internal Server Error
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "result": "Server error"
            }
        )
    finally:
        db.close()
                    