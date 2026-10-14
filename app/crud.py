"""CRUD operations for addresses."""
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.geo import KM_PER_DEGREE_LAT, haversine_km

logger = logging.getLogger(__name__)


def create_address(db: Session, data: schemas.AddressCreate) -> models.Address:
    address = models.Address(**data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    logger.info("Created address id=%s", address.id)
    return address


def get_address(db: Session, address_id: int) -> models.Address | None:
    return db.get(models.Address, address_id)


def list_addresses(db: Session, skip: int = 0, limit: int = 100) -> list[models.Address]:
    stmt = select(models.Address).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def update_address(
    db: Session, address: models.Address, data: schemas.AddressUpdate
) -> models.Address:
    # exclude_unset -> only update fields the client actually sent
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    logger.info("Updated address id=%s", address.id)
    return address


def delete_address(db: Session, address: models.Address) -> None:
    db.delete(address)
    db.commit()
    logger.info("Deleted address id=%s", address.id)


def get_addresses_within_distance(
    db: Session, latitude: float, longitude: float, distance_km: float
) -> list[models.Address]:
    """Return addresses within distance_km of the given point.

    Step 1: cheap SQL filter on a latitude band to shrink the candidate set.
    Step 2: exact Haversine check in Python.
    """
    lat_delta = distance_km / KM_PER_DEGREE_LAT
    stmt = select(models.Address).where(
        models.Address.latitude.between(latitude - lat_delta, latitude + lat_delta)
    )
    candidates = db.scalars(stmt)
    results = [
        a for a in candidates
        if haversine_km(latitude, longitude, a.latitude, a.longitude) <= distance_km
    ]
    logger.info("Nearby search found %d addresses", len(results))
    return results