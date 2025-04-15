from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from scripts.models.jwt_model import UserCreate, Token
from scripts.handlers.jwt_handler import signup_user, login_user
from scripts.constants.api_endpoints import Endpoints

authentication_router = APIRouter()

@authentication_router.post(Endpoints.AUTH_SIGNUP)
def signup(user: UserCreate):
    return signup_user(user)

@authentication_router.post(Endpoints.AUTH_LOGIN)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

