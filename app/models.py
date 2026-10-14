"""ORM models."""
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float)