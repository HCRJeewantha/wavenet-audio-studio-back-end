from models.sqlite_models import User
from request.user_requests import CreateUserRequest
from sqlalchemy.orm import Session
from database.sqlite_connection import get_db
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from services.hash_password import hash_password
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder 
from services.jwt_auth import create_token

db: Session = next(get_db())

async def create_user(request: CreateUserRequest):
    try:
        user = User(
            username=request.username,
            primary_email=request.primary_email,
            password=hash_password(request.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return JSONResponse({
            "status": True,
            "message": "User has been created successfully",
            "result": jsonable_encoder(user),
            "token": create_token(user)
        })

    except IntegrityError as e:
        # Extract the error message for better clarity
        error_info = str(e.orig)
        print(e)
        if "unique constraint" in error_info.lower():
            # Using a 422 status code for Unprocessable Entity
            raise HTTPException(status_code=422, detail="Email is already exists")

    finally:
        # Ensure the database connection is closed
        db.close()
                    