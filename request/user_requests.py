from datetime import date
from typing import  Union, Optional
from pydantic import BaseModel, Field, validator, SecretStr

class LoginUserRequest(BaseModel):
    email: Union[str, None]
    password: str

class CreateUserRequest(BaseModel):
    username: str
    primary_email: str
    password: str