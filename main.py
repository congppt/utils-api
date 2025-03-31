from contextlib import asynccontextmanager
from fastapi import FastAPI

from cache import CACHE
from database import DATABASE
import features

async def astartup():
    pass

async def ashutdown():
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE.aclose_connections()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await astartup()
    yield
    await ashutdown()

app = FastAPI(lifespan=lifespan)
for router in features.routers:
    app.include_router(router, prefix="/api")