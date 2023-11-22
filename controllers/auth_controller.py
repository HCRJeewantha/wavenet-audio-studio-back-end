from services.jwt_auth import create_token
from models.sqlite_models import User
from request.user_requests import LoginUserRequest
from sqlalchemy.orm import Session
from database.sqlite_connection import get_db
from fastapi import HTTPException, status
from services.hash_password import  verify_password
from fastapi.responses import JSONResponse
import os

otp_valid = os.getenv('OTP_VALID')
db: Session = next(get_db())

async def login_user(request: LoginUserRequest):
    try:
        user = db.query(User).filter(User.primary_email == request.email).first()

        if user and verify_password(pw=request.password, hash_pw=user.password):
            return {
                "status": True,
                "result": user,
                "message": "User login successful",
                "token": create_token(user)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username or password incorrect"
            )
        
    except HTTPException as http_exception:
            raise http_exception
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )
