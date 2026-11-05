from pydantic import BaseModel, Field
from typing import Literal, Optional


class DisasterCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)

    disaster_type: Literal[
        "flood",
        "earthquake",
        "cyclone",
        "landslide",
        "wildfire",
        "other"
    ]

    severity: Literal["low", "moderate", "high", "critical"]

    location: str = Field(min_length=2, max_length=150)

    description: str = Field(min_length=5, max_length=1000)

    status: Literal[
        "active",
        "monitoring",
        "resolved"
    ] = "active"


class DisasterResponse(DisasterCreate):
    id: int


class DisasterUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=3, max_length=100
    )
    severity: Optional[
        Literal["low", "moderate", "high", "critical"]
    ] = None
    location: Optional[str] = Field(
        default=None, min_length=2, max_length=150
    )
    description: Optional[str] = Field(
        default=None, min_length=5, max_length=1000
    )
    status: Optional[
        Literal["active", "monitoring", "resolved"]
    ] = None