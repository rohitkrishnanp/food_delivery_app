from fastapi import HTTPException, APIRouter
import uuid
from typing import Dict, List
from .restaurants import router
from app.storage import db
from app.schemas.menu import Menu, MenuResponse

router = APIRouter()


@router.post("/{restaurant_id}/menus", response_model=MenuResponse)
def create_menu(restaurant_id: str, menu: Menu):
    """Create a new menu for the specified restaurant."""

    if restaurant_id not in db.restaurants:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found.",
        )
    menu_id = str(uuid.uuid4())
    menu_dict = menu.dict()
    menu_dict["menu_id"] = menu_id
    menu_dict["restaurant_id"] = restaurant_id

    # Define _links for the response
    links = {
        "self": {"href": f"/api/restaurants/{restaurant_id}/menus/{menu_id}"},
        "items": {
            "href": f"/api/restaurants/{restaurant_id}/menus/{menu_id}/items"
        },
    }
    menu_dict["_links"] = links
    db.menu[menu_id] = menu_dict

    return menu_dict


@router.get(
    "/{restaurant_id}/menus",
    response_model=List[MenuResponse],
)
def get_menus(restaurant_id: str):
    """Retrieve all menus for the specified restaurant."""

    if restaurant_id not in db.restaurants:
        raise HTTPException(
            status_code=404,
            detail=f"No menus found for restaurant with ID {restaurant_id}.",
        )

    menus = []
    for _, menu in db.menu.items():
        if menu["restaurant_id"] == restaurant_id:
            menus.append(menu)
    return menu


@router.get(
    "/{restaurant_id}/menus/{menu_id}",
    response_model=MenuResponse,
)
def get_menu(restaurant_id: str, menu_id: str):
    """Retrieve the specified menu for the specified restaurant."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
    ):
        return db.menu[menu_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )


@router.put(
    "/{restaurant_id}/menus/{menu_id}",
    response_model=MenuResponse,
)
def update_menu(restaurant_id: str, menu_id: str, menu: Menu):
    """Update the specified menu for the specified restaurant."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
    ):
        current = db.menu[menu_id]
        updated = menu.dict(exclude_unset=True)
        for key, value in updated.items():
            if value is not None:
                current[key] = value
        db.menu[menu_id] = current
        return db.menu[menu_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )


@router.delete("/{restaurant_id}/menus/{menu_id}", status_code=204)
def delete_menu(restaurant_id: str, menu_id: str):
    """Delete the specified menu for the specified restaurant."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
    ):
        del db.menu[menu_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )
