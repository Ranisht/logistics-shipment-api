from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, Enum as SAEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class ShipmentStatus(str, Enum):
    CREATED = ("CREATED",)
    PICKED_UP = ("PICKED_UP",)
    IN_TRANSIT = ("IN_TRANSIT",)
    DELIVERED = "DELIVERED"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    tracking_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    customer_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    origin: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    destination: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[ShipmentStatus] = mapped_column(
        SAEnum(
            ShipmentStatus,
            name="shipment_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            validate_strings=True,
        ),
        nullable=False,
        default=ShipmentStatus.CREATED,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
