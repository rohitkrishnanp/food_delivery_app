from fastapi import APIRouter, HTTPException, Path
import uuid
from app.schemas.users import (
    UserResponse,
    UserRequest,
    UserLogin,
    UserLoginResponse,
)
from app.storage import db

router = APIRouter()


@router.post("/", status_code=201, response_model=UserResponse)
def add_user(user: UserRequest):
    """Add a new user to the database"""

    if user.email in db.users:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )

    user_response = UserResponse(**user.model_dump())
    user_response.id = str(uuid.uuid4())
    db.users[user_response.email] = user_response.model_dump()
    db.users[user_response.id] = user_response.model_dump()
    return user_response


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str = Path(..., title="User ID")):
    """Get a user from the database"""

    if user_id not in db.users:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    return db.users[user_id]


@router.post("/login", status_code=200, response_model=UserResponse)
def login_user(user: UserLogin):
    """Login a user"""

    if user.email not in db.users:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password. Please try again",
        )
    login = UserLoginResponse(**user.model_dump())
    login.token = str(uuid.uuid4())
    return login


@router.put("/{user_id}", status_code=201, response_model=UserResponse)
def update_user(user: UserRequest, user_id: str = Path(..., title="User ID")):
    """Update a user in the database"""

    if user_id not in db.users:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    # update the current user
    current = db.users[user_id]
    updated = user.model_dump()
    for key, value in updated.items():
        if value is not None:
            current[key] = value
    db.users[user_id] = current

    return db.users[user_id]


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str = Path(..., title="User ID")):
    """Delete a user from the database"""

    if user_id not in db.users:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    email = db.users[user_id]["email"]
    del db.users[user_id]
    del db.users[email]
