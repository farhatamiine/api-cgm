from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers.health import health_router
from routers.glucose import glucose_router 
from routers.bolus import bolus_router 
from db.database import check_connection




@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup — runs before app accepts requests
    check_connection()
    yield
    # shutdown — runs when app stops
    print("App shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(health_router,prefix="/api/v1/health")
app.include_router(glucose_router,prefix="/api/v1/glucose")
app.include_router(bolus_router,prefix="/api/v1/bolus")

