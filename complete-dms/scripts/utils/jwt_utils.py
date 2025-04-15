from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from scripts.models.jwt_model import User
from scripts.constants.api_endpoints import Endpoints
from scripts.constants import app_constants
from scripts.constants.app_configuration import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Endpoints.AUTH_LOGIN)

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("password123")
    }
}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_user_credentials(user: User) -> bool:
    stored_user = fake_users_db.get(user.username)
    if not stored_user:
        raise HTTPException(status_code=401, detail=app_constants.INVALID_CREDENTIALS)

    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail=app_constants.INVALID_CREDENTIALS)

    return True

#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail=app_constants.AUTH_TOKEN_INVALID)

        return {"username": username}

    except JWTError:
        raise HTTPException(status_code=401, detail=app_constants.AUTH_TOKEN_INVALID)
    except Exception:
        raise HTTPException(status_code=500, detail=app_constants.INTERNAL_SERVER_ERROR)


from datetime import datetime, timedelta

from jose import JWTError, jwt

# Secret key for encoding and decoding the JWT

SECRET_KEY = "your_secret_key_here"  # 🔒 Change this to a secure secret

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            return None

        return username

    except JWTError:

        return None

