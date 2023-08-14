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


class RestaurantResponse(Restaurant):
    restaurant_id: str = None


class Menu(BaseModel):
    name: str = None
    description: str = None


class MenuResponse(Menu):
    menu_id: str
    restaurant_id: str
    _links: Dict[str, Dict[str, str]]
