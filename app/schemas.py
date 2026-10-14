"""Pydantic schemas: request/response validation."""
from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Office"])
    street: str = Field(..., min_length=1, max_length=255, examples=["MG Road"])
    city: str = Field(..., min_length=1, max_length=100, examples=["Bengaluru"])
    country: str = Field(..., min_length=1, max_length=100, examples=["India"])
    postal_code: str | None = Field(None, max_length=20, examples=["560001"])
    latitude: float = Field(..., ge=-90, le=90, examples=[12.9716])
    longitude: float = Field(..., ge=-180, le=180, examples=[77.5946])


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    """All fields optional so clients can update only what changed."""
    name: str | None = Field(None, min_length=1, max_length=100)
    street: str | None = Field(None, min_length=1, max_length=255)
    city: str | None = Field(None, min_length=1, max_length=100)
    country: str | None = Field(None, min_length=1, max_length=100)
    postal_code: str | None = Field(None, max_length=20)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)


class AddressRead(AddressBase):
    id: int
    model_config = ConfigDict(from_attributes=True)