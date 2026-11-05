from backend.app.core.database import Base, engine
from backend.app.models import disaster
from backend.app.models import hazard_zone
from fastapi import FastAPI

from backend.app.api.routes import evacuation
from backend.app.api.routes.disasters import router as disaster_router
from backend.app.api.routes.hazard_zones import router as hazard_zone_router

app = FastAPI(
    title="AI-Powered Adaptive Disaster Management System",
    description=(
        "Backend API for disaster monitoring, "
        "hazard management and intelligent evacuation."
    ),
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)
app.include_router(disaster_router)
app.include_router(hazard_zone_router)
app.include_router(evacuation.router)

@app.get("/")
def root():
    return {
        "message": "Disaster Management API is running",
        "project": "AI-Powered Adaptive Disaster Management System",
        "version": "1.0.0",
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "disaster-management-backend",
    }

