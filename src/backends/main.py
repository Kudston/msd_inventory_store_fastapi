from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.backends.database import engine, sessionLocal, open_db_connections, close_db_connections
from src.backends import models
from src.backends.Initialize_platform import initialize_superuser
from src.backends.users.router import router as user_router
from src.backends.products.router import router as product_router
from src.backends.orders.router import router as order_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ##open db connections
    open_db_connections()
    initialize_superuser()
    yield
    ##close db connections
    close_db_connections()

app = FastAPI(lifespan=lifespan)

allowed_origins = [
    "http://172.19.0.4:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log the validation errors
    logger.error(f"Validation error: {exc.errors()}")
    
    # Return a custom JSON response with the validation errors
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )

@app.get('/')
def home():
    return ({'detail':'welcome to msd inventory system'})