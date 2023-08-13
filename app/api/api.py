from fastapi import APIRouter, Depends
from app.api.endpoints import users
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_router = APIRouter()

api_router.include_router(
    users.router, prefix="/users", tags=["users"]
)
