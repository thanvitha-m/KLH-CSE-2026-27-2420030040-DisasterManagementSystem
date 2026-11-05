
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.hazard_zone import HazardZone
from backend.app.schemas.hazard_zone import (
    HazardZoneCreate,
    HazardZoneResponse,
    HazardZoneUpdate,
)

router = APIRouter(
    prefix="/api/v1/hazard-zones",
    tags=["Hazard Zone Management"],
)


# CREATE HAZARD ZONE
@router.post(
    "/",
    response_model=HazardZoneResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hazard_zone(
    hazard: HazardZoneCreate,
    db: Session = Depends(get_db),
):
    new_hazard = HazardZone(**hazard.model_dump())

    db.add(new_hazard)
    db.commit()
    db.refresh(new_hazard)

    return new_hazard


# GET ALL HAZARD ZONES
@router.get("/", response_model=list[HazardZoneResponse])
def get_all_hazard_zones(db: Session = Depends(get_db)):
    return db.query(HazardZone).order_by(HazardZone.id).all()


# GET HAZARD ZONE BY ID
@router.get("/{hazard_id}", response_model=HazardZoneResponse)
def get_hazard_zone(
    hazard_id: int,
    db: Session = Depends(get_db),
):
    hazard = db.query(HazardZone).filter(
        HazardZone.id == hazard_id
    ).first()

    if hazard is None:
        raise HTTPException(
            status_code=404,
            detail="Hazard zone not found",
        )

    return hazard


# UPDATE HAZARD ZONE
@router.patch(
    "/{hazard_id}",
    response_model=HazardZoneResponse,
)
def update_hazard_zone(
    hazard_id: int,
    updates: HazardZoneUpdate,
    db: Session = Depends(get_db),
):
    hazard = db.query(HazardZone).filter(
        HazardZone.id == hazard_id
    ).first()

    if hazard is None:
        raise HTTPException(
            status_code=404,
            detail="Hazard zone not found",
        )

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value is not None:
            setattr(hazard, field, value)

    db.commit()
    db.refresh(hazard)

    return hazard


# DELETE HAZARD ZONE
@router.delete("/{hazard_id}")
def delete_hazard_zone(
    hazard_id: int,
    db: Session = Depends(get_db),
):
    hazard = db.query(HazardZone).filter(
        HazardZone.id == hazard_id
    ).first()

    if hazard is None:
        raise HTTPException(
            status_code=404,
            detail="Hazard zone not found",
        )

    db.delete(hazard)
    db.commit()

    return {
        "message": "Hazard zone deleted successfully",
        "id": hazard_id,
    }
