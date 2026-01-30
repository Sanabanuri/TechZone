from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import Cart, CartItem, Product, User
from app.schemas import ShowCart, CartAdd

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_to_cart(cart_data: CartAdd, user_id:int, session:Session = Depends(get_session)):
    cart = session.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id = user_id)

        session.add(cart)
        session.commit()
        session.refresh(cart)

    product = session.query(Product).filter(Product.id == cart_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    new_item = CartItem(cart_id = cart.id, product_id = cart_data.product_id, quantity = cart_data.quantity)

    session.add(new_item)
    session.commit()

    return {"message":"Item added to cart successfully"}