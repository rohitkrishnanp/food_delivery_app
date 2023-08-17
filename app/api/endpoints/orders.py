from fastapi import APIRouter, HTTPException, Query, Path
from typing import Dict, List
import uuid
from app.storage import db
from app.schemas.orders import Order, OrderResponse

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=OrderResponse,
    response_model_exclude_none=True,
)
def create_order(order: Order):
    """Create a new order in the database."""

    order_id = str(uuid.uuid4())

    order_dict = order.model_dump()
    order_dict["order_id"] = order_id

    # Define _links for the response
    links = {"self": {"href": f"/api/orders/{order_id}"}}
    order_dict["_links"] = links

    db.orders[order_id] = order_dict

    return order_dict


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    response_model_exclude_none=True,
)
def get_order(order_id: str):
    """Get an order from the database."""

    if order_id not in db.orders:
        raise HTTPException(
            status_code=404, detail=f"Order with the given orderId not found."
        )
    return db.orders[order_id]


@router.get(
    "/", response_model=List[OrderResponse], response_model_exclude_none=True
)
def get_orders_for_customer(
    customer_id: str = Query(..., description="Customer ID")
):
    """Get all orders from the customer"""

    orders = []
    for _, order in db.orders.items():
        if order["customer_id"] == customer_id:
            orders.append(order)

    return orders


@router.put(
    "/order_id}/status/{status}",
    response_model=OrderResponse,
    response_model_exclude_none=True,
)
def update_order_status(
    order_id: str, status: str = Path(..., description="Status of the order")
):
    """Update the status of the order"""

    if order_id not in db.orders:
        raise HTTPException(
            status_code=404, detail=f"Order with the given orderId not found."
        )

    order = db.orders[order_id]
    order["status"] = status

    return order


@router.delete("/{order_id}")
def cancel_order(order_id: str):
    """Cancel the order"""

    if order_id not in db.orders:
        raise HTTPException(
            status_code=404, detail=f"Order with the given orderId not found."
        )

    del db.orders[order_id]
    return {"message": "Order cancelled successfully"}
