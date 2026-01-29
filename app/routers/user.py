from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import UserCreate, ShowUser, UpdateUser
from app.models import User
from typing import List


router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(user : UserCreate, session: Session = Depends(get_session)):
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowUser])
async def get_all_user(session: Session = Depends(get_session)):
    users = session.query(User).all()
    return users


@router.put("/{user_id}",status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser)
async def update_user(user_id: int, user_update: UpdateUser, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    update_user_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_user_data.items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    session.delete(user)
    session.commit()

    return None