import os
import jwt
import configparser
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '/.cfg')

key = config['JWT']['SECRET_KEY']
algorithm = config['JWT']['ALGORITHM']
exp = int(config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES'])


def create_token(user):

    current_time = datetime.now(tz=timezone.utc)
    payload_data = {
        "iat": current_time,
        "nbf": current_time,
        "exp": current_time + timedelta(minutes=exp),
        "sub": str(user.id),
    }

    token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm=algorithm
    )
    return token


def decode_token(token):
    try:
        decode = jwt.decode(token, key, algorithms=algorithm)
        return decode
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "result": "Token Expired"
            })
    except jwt.exceptions.ImmatureSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "result": "Invalid Token (Immature Signature)"
            }
        )
