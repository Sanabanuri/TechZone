from pydantic import BaseModel
from typing import List, Optional

class ProductCreate(BaseModel):
    name : str
    description : str
    price : float
    image_url : str

class ProductUpdate(BaseModel):
    name : str
    description : str
    price : float
    image_url : str

class ShowProduct(BaseModel):
    name : str
    description : str
    price : float
    image_url : str
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email : str
    password : str

class UpdateUser(BaseModel):
    email : str
    password : str

class ShowUser(BaseModel):
    email : str
    
    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    product_id: int
    quantity : int

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemSchema]

class ShowOrderDetail(BaseModel):
    product_id: int
    quantity: int
    price: float 
    
    class Config:
        from_attributes = True


class ShowOrder(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    order_details : List[ShowOrderDetail]=[]

    class Config:
        from_attributes = True

# Cart Schemas

class CartAdd(BaseModel):
    product_id : int
    quantity : int

class ShowCartItem(BaseModel):
    product_id : int
    quantity : int

    class Config:
        from_attributes = True


class ShowCart(BaseModel):
    id : int
    user_id : int
    cart_items : List[ShowCartItem]=[]

    class Config:
        from_attributes = True