from pydantic import BaseModel


class MenuItem(BaseModel):
    name: str = None
    price: float = None
    description: str = None


class MenuItemResponse(MenuItem):
    item_id: str = None
    menu_id: str = None
    restaurant_id: str = None
    _links: dict = None
