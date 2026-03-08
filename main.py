from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import check_connection, create_tables
from routers.basal import basal_router
from routers.bolus import bolus_router
from routers.glucose import glucose_router
from routers.health import health_router
from routers.hypo import hypo_router
from routers.insight import insights_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup — runs before app accepts requests
    check_connection()
    create_tables()
    yield
    # shutdown — runs when app stops
    print("App shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, prefix="/api/v1/health")
app.include_router(glucose_router, prefix="/api/v1/glucose")
app.include_router(bolus_router, prefix="/api/v1/bolus")
app.include_router(basal_router, prefix="/api/v1/basal", tags=["basal"])
app.include_router(hypo_router, prefix="/api/v1/hypo", tags=["hypo"])
app.include_router(insights_router, prefix="/api/v1/insights", tags=["insights"])
