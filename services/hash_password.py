from passlib.context import CryptContext
from models.sqlite_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(pw: str, hash_pw: User.password):
    return pwd_context.verify(pw, hash_pw)

def hash_password(password):
    return pwd_context.hash(password)