from pydantic import BaseModel
from .users import Location


class OrderItem(BaseModel):
    menu_item_id: str = None
    name: str = None
    quantity: int = None
    price: float = None
    subtotal: float = None


class Order(BaseModel):
    customer_id: str = None
    restaurant_id: str = None
    items: list[OrderItem] = None
    customer_location: Location = None
    payment_method: str = None
    total: float = None
    status: str = None
    _links: dict = None
