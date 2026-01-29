from pydantic import BaseModel

class ProductCreate(BaseModel):
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