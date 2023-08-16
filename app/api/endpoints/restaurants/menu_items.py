from fastapi import HTTPException, APIRouter
from typing import List
import uuid
from app.storage import db
from app.schemas.menu_items import MenuItem, MenuItemResponse

router = APIRouter()


@router.post(
    "/{restaurant_id}/menus/{menu_id}/items",
    response_model=MenuItemResponse,
    response_model_exclude_none=True,
)
def create_menu_item(restaurant_id: str, menu_id: str, menu_item: MenuItem):
    """Create a new menu item for the specified menu."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
    ):
        item_id = str(uuid.uuid4())
        menu_item_dict = menu_item.model.dumps()
        menu_item_dict["item_id"] = item_id
        menu_item_dict["menu_id"] = menu_id
        menu_item_dict["restaurant_id"] = restaurant_id

        # Define _links for the response
        links = {
            "self": {
                "href": f"/api/restaurants/{restaurant_id}/menus/{menu_id}/items/{item_id}"
            }
        }
        menu_item_dict["_links"] = links

        db.menu_items[item_id] = menu_item_dict

        return menu_item_dict
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )


@router.get(
    "/{restaurant_id}/menus/{menu_id}/items",
    response_model=List[MenuItemResponse],
    response_model_exclude_none=True,
)
def get_menu_items(restaurant_id: str, menu_id: str):
    """Retrieve all menu items for the specified menu."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
    ):
        menu_items = []
        for _, item in db.menu_items.items():
            if item["menu_id"] == menu_id:
                menu_items.append(item)
        return menu_items
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )


@router.get(
    "/{restaurant_id}/menus/{menu_id}/items/{item_id}",
    response_model=MenuItemResponse,
    response_model_exclude_none=True,
)
def get_menu_item(restaurant_id: str, menu_id: str, item_id: str):
    """Retrieve the specified menu item."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
        and item_id in db.menu_items
    ):
        return db.menu_items[item_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu with ID {menu_id} not found for restaurant with ID {restaurant_id}.",
        )


@router.put(
    "/{restaurant_id}/menus/{menu_id}/items/{item_id}",
    response_model=MenuItemResponse,
    response_model_exclude_none=True,
)
def update_menu_item(
    restaurant_id: str, menu_id: str, item_id: str, menu_item: MenuItem
):
    """Update the specified menu item."""
    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
        and item_id in db.menu_items
    ):
        current = db.menu_items[item_id]
        updated = menu_item.model.dumps()
        for key, value in updated.items():
            if value is not None:
                current[key] = value
        db.menu_items[item_id] = current

        return db.menu_items[item_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu item with the given item ID not found.",
        )


@router.delete(
    "/{restaurant_id}/menus/{menu_id}/items/{item_id}", status_code=204
)
def delete_menu_item(restaurant_id: str, menu_id: str, item_id: str):
    """Delete the specified menu item."""

    if (
        menu_id in db.menu
        and db.menu[menu_id]["restaurant_id"] == restaurant_id
        and item_id in db.menu_items
    ):
        del db.menu_items[item_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Menu item with the given item ID not found.",
        )
