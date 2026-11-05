
from sqlalchemy import Column, Integer, String, Float, Text
from backend.app.core.database import Base


class HazardZone(Base):
    __tablename__ = "hazard_zones"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    hazard_type = Column(String(30), nullable=False)

    severity = Column(String(20), nullable=False)

    location = Column(String(150), nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    radius_km = Column(Float, nullable=False)

    description = Column(Text, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="active"
    )
