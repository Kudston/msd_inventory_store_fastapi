from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import engine, sessionLocal, open_db_connections, close_db_connections
from src import models
from src.users.router import router as user_router
from src.products.router import router as product_router
from src.orders.router import router as order_router

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ##open db connections
    open_db_connections()
    yield
    ##close db connections
    close_db_connections()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

@app.get('/')
def home():
    return ({'detail':'welcome to msd inventory system'})