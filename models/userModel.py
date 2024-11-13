from pydantic import BaseModel
from enum import Enum

class Role(str,Enum):
    user="user"
    admin="admin"

class User(BaseModel):
    name:str
    email:str
    password:str
    role:Role

class UserUpdate(BaseModel):
    name: str = None
    password: str = None
    email: str = None

