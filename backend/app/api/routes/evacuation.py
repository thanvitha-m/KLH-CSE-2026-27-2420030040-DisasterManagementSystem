from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app.core.database import get_db
from backend.app.models.hazard_zone import HazardZone
from backend.app.services.geographic_routing import recommend_geographic_route
from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.evacuation_engine import (
    DEMO_ROUTES,
    recommend_route
)

router = APIRouter(
    prefix="/api/v1/evacuation",
    tags=["Evacuation"]
)


class RouteConditions(BaseModel):
    route_a_hazard: int = Field(default=4, ge=0, le=5)
    route_a_crowd: float = Field(default=0.8, ge=0, le=1)
    route_a_blocked: bool = False

    route_b_hazard: int = Field(default=1, ge=0, le=5)
    route_b_crowd: float = Field(default=0.2, ge=0, le=1)
    route_b_blocked: bool = False


@router.get("/recommend")
def get_recommended_route():
    return recommend_route(DEMO_ROUTES)


@router.post("/recommend")
def adaptive_recommendation(conditions: RouteConditions):
    routes = [route.copy() for route in DEMO_ROUTES]

    routes[0]["hazard_level"] = conditions.route_a_hazard
    routes[0]["crowd_density"] = conditions.route_a_crowd
    routes[0]["blocked"] = conditions.route_a_blocked

    routes[1]["hazard_level"] = conditions.route_b_hazard
    routes[1]["crowd_density"] = conditions.route_b_crowd
    routes[1]["blocked"] = conditions.route_b_blocked

    return recommend_route(routes)

@router.get("/geographic-recommend")
def geographic_recommendation(
    db: Session = Depends(get_db)
):
    hazards = db.query(HazardZone).filter(
        HazardZone.status.in_(["active", "monitoring"])
    ).all()

    hazard_data = [
        {
            "name": hazard.name,
            "latitude": hazard.latitude,
            "longitude": hazard.longitude,
            "radius_km": hazard.radius_km,
            "severity": hazard.severity,
            "status": hazard.status,
        }
        for hazard in hazards
    ]

    result = recommend_geographic_route(hazard_data)
    result["hazard_zones_analyzed"] = len(hazard_data)

    return result
