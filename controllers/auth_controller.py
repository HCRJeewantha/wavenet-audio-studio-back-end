from services.jwt_auth import create_token
from models.sqlite_models import User
from request.user_requests import LoginUserRequest
from sqlalchemy.orm import Session
from database.sqlite_connection import get_db
from fastapi import HTTPException
from services.hash_password import  verify_password
from fastapi.responses import JSONResponse
import os

otp_valid = os.getenv('OTP_VALID')
db: Session = next(get_db())

async def login_user(request: LoginUserRequest):

    try:
        user: User = db.query(User)
        user: User = user.filter(User.primary_email == request.email).first()
            
        if user:
            if verify_password(pw=request.password, hash_pw=user.password):
                return {
                    "status": True,
                    "result": user,
                    "message": "User login successful",
                    "token": create_token(user)
                }

            else:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": False,
                        "message": "Username or Password Incorrect"
                    }
                )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail={
                "status": False,
                "result": str(e)
            }
        )
    finally:
        db.close()
