from pydantic import BaseModel


class Menu(BaseModel):
    name: str = None
    description: str = None


class MenuResponse(Menu):
    menu_id: str = None
    restaurant_id: str = None
    _links: dict = None
