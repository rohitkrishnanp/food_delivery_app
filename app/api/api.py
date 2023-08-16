from fastapi import APIRouter, Depends
from app.api.endpoints import users
from app.api.endpoints.restaurants import restaurants
from app.api.endpoints.restaurants import menu
from app.api.endpoints.restaurants import menu_items
from app.api.endpoints import orders
from app.api.endpoints import rate

from app.auth.authorization import authorization_scheme

# api_router = APIRouter(dependencies=[Depends(authorization_scheme)])
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    restaurants.router, prefix="/restaurants", tags=["Restaurants"]
)

api_router.include_router(menu.router, prefix="/restaurants", tags=["Menus"])

api_router.include_router(
    menu_items.router, prefix="/restaurants", tags=["Menu Items"]
)

api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])

api_router.include_router(rate.router, tags=["Ratings"])
