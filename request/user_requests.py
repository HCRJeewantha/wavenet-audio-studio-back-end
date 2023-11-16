from datetime import date
from typing import  Union, Optional
from pydantic import BaseModel, Field, validator, SecretStr

class LoginUserRequest(BaseModel):
    email: Union[str, None]
    password: str


class CreateUserRequest(BaseModel):
    username: str
    first_name: str = Field(..., min_length=1)
    last_name: Optional[str] = None
    primary_email: str
    password: str