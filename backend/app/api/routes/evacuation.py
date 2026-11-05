

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
