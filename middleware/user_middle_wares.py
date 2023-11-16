from collections import namedtuple
import os
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session


JWT_SECRET = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
exp = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

class Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(Authorization, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        bearer: HTTPAuthorizationCredentials = await super(Authorization, self).__call__(request)
        if bearer:
            try:
                decode = jwt.decode(bearer.credentials,
                                    JWT_SECRET,
                                    algorithms=JWT_ALGORITHM,
                                    )
                tuples = namedtuple("auth", decode.keys())(*decode.values())
                yield (tuples)
            except jwt.InvalidAudienceError:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": False,
                        "result": "Unauthorized Access , Unable to verify the audience"
                    }
                )

            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=401,
                    detail={
                        "status": False,
                        "result": "Token Expired"
                    })

            except jwt.exceptions.ImmatureSignatureError:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": False,
                        "result": "Invalid Token (Immature Signature)"
                    }
                )

            except jwt.exceptions.DecodeError as e:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": False,
                        "result": str(e)
                    }
                )

            except jwt.exceptions.MissingRequiredClaimError:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": False,
                        "result": "Unauthorized Token , User does'nt have valid user role"
                    }
                )

            except jwt.InvalidTokenError as e:
                raise HTTPException(
                    status_code=401,
                    detail={
                        "status": False,
                        "result": f"Invalid Token {str(e)}"
                    }
                )

        else:
            raise HTTPException(
                status_code=403,
                detail={
                    "status": False,
                    "result": "Authorization Token Required"
                })
