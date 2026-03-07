from fastapi import FastAPI
from routers.health import health_router
from routers.glucose import glucose_router 
from routers.bolus import bolus_router 



app = FastAPI()
app.include_router(health_router,prefix="/api/v1/health")
app.include_router(glucose_router,prefix="/api/v1/glucose")
app.include_router(bolus_router,prefix="/api/v1/bolus")