from pydantic import BaseModel
class Location(BaseModel):
    name: str = None
    latitude: float = None
    longitude: float = None

class UserRequest(BaseModel):
    name: str = None
    email: str = None
    contact: str = None
    role: str = None
    locations: list[Location] = None

class UserResponse(BaseModel):
    id : str = None
    name: str  = None
    email: str = None
    contact: str = None
    role: str = None
    locations: list[Location] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(UserResponse):
    token : str