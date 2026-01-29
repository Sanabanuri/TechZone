from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import Product
from app.schemas import ProductCreate, ShowProduct
from typing import List

router = APIRouter(prefix="/product", tags=["Products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowProduct)
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    new_product = Product(**product.model_dump())

    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@router.get("/", status_code=status.HTTP_200_OK,response_model=List[ShowProduct])
async def get_all_products(session: Session = Depends(get_session)):
    products = session.query(Product).all()

    return products

