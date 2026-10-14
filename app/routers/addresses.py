"""Address endpoints."""
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", response_model=schemas.AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(data: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, data)


@router.get("/", response_model=list[schemas.AddressRead])
def list_addresses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.list_addresses(db, skip, limit)


# NOTE: must be defined BEFORE "/{address_id}" or "nearby" is parsed as an id
@router.get("/nearby", response_model=list[schemas.AddressRead])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0, description="Search radius in km"),
    db: Session = Depends(get_db),
):
    return crud.get_addresses_within_distance(db, latitude, longitude, distance_km)


@router.get("/{address_id}", response_model=schemas.AddressRead)
def get_address(address_id: int, db: Session = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if not address:
        logger.warning("Address id=%s not found", address_id)
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.patch("/{address_id}", response_model=schemas.AddressRead)
def update_address(address_id: int, data: schemas.AddressUpdate, db: Session = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return crud.update_address(db, address, data)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    crud.delete_address(db, address)