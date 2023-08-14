from pydantic import BaseModel

class Location(BaseModel):
    latitude: float = None
    longitude: float = None

class Restaurant(BaseModel):
    name: str = None
    description: str = None
    contact: str = None
    location: Location  = None


class RestaurantResponse(Restaurant):
    restaurant_id: str = None