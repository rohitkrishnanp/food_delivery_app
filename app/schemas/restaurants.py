from pydantic import BaseModel
from typing import Dict, List


class Location(BaseModel):
    latitude: float = None
    longitude: float = None


class Restaurant(BaseModel):
    name: str = None
    description: str = None
    contact: str = None
    location: Location = None
    rating: int = 5


class RestaurantResponse(Restaurant):
    restaurant_id: str = None
