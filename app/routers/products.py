from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import Product
from app.schemas import ProductCreate, ShowProduct, ProductUpdate
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


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ShowProduct)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    return product

@router.put("/{product_id}", status_code=status.HTTP_201_CREATED, response_model=ShowProduct)
async def update_product(product_id: int, update_product:ProductUpdate, session: Session = Depends(get_session)):
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    product_data = update_product.model_dump(exclude_unset=True)

    for key, value in product_data.items():
        setattr(product, key, value)

    session.commit()
    session.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, session: Session = Depends(get_session)):
    product = session.query(Product).filter(Product.id == product_id).first()

    session.delete(product)
    session.commit()

    return None