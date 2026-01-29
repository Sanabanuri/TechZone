from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import user,products


app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(user.router)

app.include_router(products.router)

