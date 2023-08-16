from fastapi import APIRouter, HTTPException, Query
from fastapi import HTTPException
import uuid

from app.schemas.restaurants import Restaurant, RestaurantResponse

from app.storage import db

router = APIRouter()


@router.post("/", response_model=RestaurantResponse, response_model_exclude_none=True)
def create_restaurant(restaurant: Restaurant):
    """Add a new restaurant to the database"""

    response = RestaurantResponse(**restaurant.model_dump())
    response.restaurant_id = str(uuid.uuid4())
    db.restaurants[response.restaurant_id] = response.model_dump()
    return response


@router.get("/{restaurant_id}", response_model=RestaurantResponse, response_model_exclude_none=True)
def get_restaurant(restaurant_id: str):
    """Get a restaurant from the database"""

    if restaurant_id in db.restaurants:
        return db.restaurants[restaurant_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )


@router.get("/", response_model_exclude_none=True)
def get_restaurants_nearby(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius: int = Query(..., description="Radius in kilometers"),
):
    """Get restaurants near the specified location within the given radius"""

    # Implement the logic to retrieve restaurants near the specified location within the given radius
    # For this example, we return the entire list of restaurants
    list_of_restaurants = []
    for restaurant in db.restaurants.values():
        list_of_restaurants.append(restaurant)

    return list_of_restaurants


@router.put("/{restaurant_id}", response_model=RestaurantResponse, response_model_exclude_none=True)
def update_restaurant(restaurant_id: str, restaurant: Restaurant):
    """Update a restaurant in the database"""

    if restaurant_id not in db.restaurants:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )

    # update the current restaurant
    current = db.restaurants[restaurant_id]
    updated = restaurant.model_dump()
    for key, value in updated.items():
        if value is not None:
            current[key] = value
    db.restaurants[restaurant_id] = current
    return db.restaurants[restaurant_id]


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: str):
    """Delete a restaurant from the database"""

    if restaurant_id not in db.restaurants:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )

    del db.restaurants[restaurant_id]
