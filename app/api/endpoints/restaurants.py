from fastapi import APIRouter, HTTPException, Query
from fastapi import APIRouter, HTTPException
import uuid

from app.schemas.restaurants import Restaurant, RestaurantResponse

router = APIRouter()

# using a simple in memory db for now
restaurants_storage = {}


@router.post("/", response_model=RestaurantResponse)
def create_restaurant(restaurant: Restaurant):
    """Add a new restaurant to the database"""

    response = RestaurantResponse(**restaurant.model_dump())
    response.restaurant_id = str(uuid.uuid4())
    restaurants_storage[response.restaurant_id] = response.model_dump()
    return response


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: str):
    """Get a restaurant from the database"""

    if restaurant_id in restaurants_storage:
        return restaurants_storage[restaurant_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )


@router.get("/")
def get_restaurants_nearby(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius: int = Query(..., description="Radius in kilometers"),
):
    """Get restaurants near the specified location within the given radius"""

    # Implement the logic to retrieve restaurants near the specified location within the given radius
    # For this example, we return the entire list of restaurants
    list_of_restaurants = []
    for restaurant in restaurants_storage.values():
        list_of_restaurants.append(restaurant)

    return list_of_restaurants


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: str, restaurant: Restaurant):
    """Update a restaurant in the database"""

    if restaurant_id not in restaurants_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )

    # update the current restaurant
    current = restaurants_storage[restaurant_id]
    updated = restaurant.model_dump()
    for key, value in updated.items():
        if value is not None:
            current[key] = value
    restaurants_storage[restaurant_id] = current
    return restaurants_storage[restaurant_id]


@router.delete("/api/restaurants/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: str):
    """Delete a restaurant from the database"""

    if restaurant_id not in restaurants_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )

    del restaurants_storage[restaurant_id]
