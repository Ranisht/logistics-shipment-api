from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.shipment import ShipmentStatus


class ShipmentStatusHistory(Base):
    __tablename__ = "shipment_status_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    shipment_id: Mapped[int] = mapped_column(
        ForeignKey("shipments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    old_status: Mapped[ShipmentStatus] = mapped_column(
        SAEnum(
            ShipmentStatus,
            name="shipment_status",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
            validate_strings=True,
        ),
        nullable=False,
    )

    new_status: Mapped[ShipmentStatus] = mapped_column(
        SAEnum(
            ShipmentStatus,
            name="shipment_status",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
            validate_strings=True,
        ),
        nullable=False,
    )

    changed_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="system",
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )