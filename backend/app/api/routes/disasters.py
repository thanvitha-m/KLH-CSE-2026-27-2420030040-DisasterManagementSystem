from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.disaster import Disaster
from backend.app.schemas.disaster import (
    DisasterCreate,
    DisasterResponse,
    DisasterUpdate,
)

router = APIRouter(
    prefix="/api/v1/disasters",
    tags=["Disaster Management"],
)


# CREATE DISASTER
@router.post(
    "/",
    response_model=DisasterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_disaster(
    disaster: DisasterCreate,
    db: Session = Depends(get_db),
):
    new_disaster = Disaster(**disaster.model_dump())

    db.add(new_disaster)
    db.commit()
    db.refresh(new_disaster)

    return new_disaster



# GET ALL DISASTERS WITH FILTERING
@router.get("/", response_model=list[DisasterResponse])
def get_all_disasters(
    disaster_type: Literal[
        "flood",
        "earthquake",
        "cyclone",
        "landslide",
        "wildfire",
        "other"
    ] | None = Query(default=None),

    severity: Literal[
        "low",
        "moderate",
        "high",
        "critical"
    ] | None = Query(default=None),

    status_filter: Literal[
        "active",
        "monitoring",
        "resolved"
    ] | None = Query(default=None, alias="status"),

    db: Session = Depends(get_db),
):
    query = db.query(Disaster)

    if disaster_type:
        query = query.filter(
            Disaster.disaster_type == disaster_type
        )

    if severity:
        query = query.filter(
            Disaster.severity == severity
        )

    if status_filter:
        query = query.filter(
            Disaster.status == status_filter
        )

    return query.order_by(Disaster.id).all()


# GET DISASTER BY ID
@router.get("/{disaster_id}", response_model=DisasterResponse)
def get_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
):
    disaster = db.query(Disaster).filter(
        Disaster.id == disaster_id
    ).first()

    if disaster is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disaster record not found",
        )

    return disaster


# UPDATE DISASTER
@router.patch(
    "/{disaster_id}",
    response_model=DisasterResponse,
)
def update_disaster(
    disaster_id: int,
    updates: DisasterUpdate,
    db: Session = Depends(get_db),
):
    disaster = db.query(Disaster).filter(
        Disaster.id == disaster_id
    ).first()

    if disaster is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disaster record not found",
        )

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value is not None:
            setattr(disaster, field, value)

    db.commit()
    db.refresh(disaster)

    return disaster


# DELETE DISASTER
@router.delete("/{disaster_id}")
def delete_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
):
    disaster = db.query(Disaster).filter(
        Disaster.id == disaster_id
    ).first()

    if disaster is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disaster record not found",
        )

    db.delete(disaster)
    db.commit()

    return {
        "message": "Disaster record deleted successfully",
        "id": disaster_id,
    }
