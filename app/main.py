"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.logging_config import setup_logging
from app.routers import addresses

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # create tables on startup
    logger.info("Database tables ready")
    yield


app = FastAPI(
    title="Address Book API",
    description="Create, update, delete and search addresses by distance.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(addresses.router)