from fastapi import FastAPI
from contextlib import asynccontextmanager
from .kafka import kafka_start, kafka_stop

ml_models = {}

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Configure application lifespan behavior."""
    await kafka_start()
    yield
    await kafka_stop()
    ml_models.clear()
