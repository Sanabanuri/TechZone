from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models import Order, OrderDetail, Product
from app.schemas import OrderCreate, ShowOrder, ShowOrder
from app.database import get_session
from typing import List
router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowOrder)
async def place_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(user_id=order.user_id, total_price=0.0)
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    current_total_amount = 0.0
    for item in order.items:
        product = session.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"product {item.product_id} not found")

        new_detail = OrderDetail(order_id = new_order.id,product_id = product.id,
        quantity = item.quantity,
        price = product.price)

        session.add(new_detail)

        current_total_amount += (product.price * item.quantity)
        new_order.total_price = current_total_amount

    session.commit()
    session.refresh(new_order)

    return new_order

@router.get("/", status_code=status.HTTP_200_OK,response_model=List[ShowOrder])
async def read_all_orders(session: Session = Depends(get_session)):
    orders = session.query(Order).options(joinedload(Order.order_detail)).all()
    return orders

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=ShowOrder)
async def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).options(joinedload(Order.order_detail)).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return order

