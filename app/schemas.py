from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic.types import conint

class User(BaseModel):
    email: EmailStr
    password: str

class UsersResponse(BaseModel):
    id: int
    email: EmailStr 
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str 
    price: int
    inventory: int
    buyer_id: int
    buyer: UsersResponse

    class Config:
        from_attributes = True


class Product(BaseModel):
    name: str 
    price: int
    inventory: int
    # buyer_id: int
    # buyer: UsersResponse

class ProductOut(BaseModel):
    Product: ProductResponse
    Favorite: int

    class Config:
        from_attributes = True

class CreateProduct(Product):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # id: Optional[str] = None
    id: str

class Favorite(BaseModel):
    product_id: int
    dir: conint(le=1)
