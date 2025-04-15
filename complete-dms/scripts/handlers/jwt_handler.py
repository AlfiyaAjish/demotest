from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from scripts.utils.jwt_utils import hash_password, verify_password, create_access_token
from scripts.models.jwt_model import UserCreate, Token

fake_users_db = {}


def signup_user(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "password": hashed_password
    }
    return {"message": "User created successfully"}


def login_user(form_data: OAuth2PasswordRequestForm) -> Token:
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")

