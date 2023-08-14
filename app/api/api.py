from fastapi import APIRouter, Depends
from app.api.endpoints import users
from app.api.endpoints.restaurants import restaurants
from app.auth.authorization import authorization_scheme

# api_router = APIRouter(dependencies=[Depends(authorization_scheme)])
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    restaurants.router, prefix="/restaurants", tags=["restaurants"]
)
