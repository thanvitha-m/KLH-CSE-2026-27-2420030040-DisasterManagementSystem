
from pydantic import BaseModel, Field
from typing import Literal, Optional


class HazardZoneCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)

    hazard_type: Literal[
        "flood",
        "fire",
        "earthquake",
        "landslide",
        "chemical_leak",
        "other"
    ]

    severity: Literal[
        "low",
        "moderate",
        "high",
        "critical"
    ]

    location: str = Field(min_length=2, max_length=150)

    latitude: float = Field(ge=-90, le=90)

    longitude: float = Field(ge=-180, le=180)

    radius_km: float = Field(gt=0, le=100)

    description: str = Field(min_length=5, max_length=1000)

    status: Literal[
        "active",
        "monitoring",
        "cleared"
    ] = "active"


class HazardZoneResponse(HazardZoneCreate):
    id: int


class HazardZoneUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=3, max_length=100
    )

    severity: Optional[
        Literal["low", "moderate", "high", "critical"]
    ] = None

    location: Optional[str] = Field(
        default=None, min_length=2, max_length=150
    )

    latitude: Optional[float] = Field(
        default=None, ge=-90, le=90
    )

    longitude: Optional[float] = Field(
        default=None, ge=-180, le=180
    )

    radius_km: Optional[float] = Field(
        default=None, gt=0, le=100
    )

    description: Optional[str] = Field(
        default=None, min_length=5, max_length=1000
    )

    status: Optional[
        Literal["active", "monitoring", "cleared"]
    ] = None
