from sqlalchemy import Column, Integer, String, Text
from backend.app.core.database import Base


class Disaster(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    disaster_type = Column(String(30), nullable=False)

    severity = Column(String(20), nullable=False)

    location = Column(String(150), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="active"
    )