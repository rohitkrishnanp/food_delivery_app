from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Dict, List
from fastapi.responses import JSONResponse
from app.storage import db

router = APIRouter()


@router.post("/api/restaurants/{restaurant_id}/ratings")
def rate_restaurant(restaurant_id: str, rating: int = Query(..., ge=1, le=5)):
    """Rate a restaurant"""

    if restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # for simplicity directly adding the rating
    db.restaurants[restaurant_id]["rating"] = rating
    return db.restaurants[restaurant_id]


@router.post("/api/orders/{order_id}/ratings")
def rate_order(order_id: str, rating: int = Query(..., ge=1, le=5)):
    """Rate an order"""

    if order_id not in db.order_id:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # for simplicity directly adding the rating
    db.orders[order_id]["rating"] = rating
    return db.orders[order_id]
