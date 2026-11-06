from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.shipment import Shipment, ShipmentStatus
from app.models.shipment_status_history import (
    ShipmentStatusHistory,
)
from app.repositories.shipment_repository import (
    ShipmentRepository,
)
from fastapi import HTTPException


ALLOWED_TRANSITIONS = {
    ShipmentStatus.CREATED: [
        ShipmentStatus.PICKED_UP,
    ],
    ShipmentStatus.PICKED_UP: [
        ShipmentStatus.IN_TRANSIT,
    ],
    ShipmentStatus.IN_TRANSIT: [
        ShipmentStatus.DELIVERED,
    ],
    ShipmentStatus.DELIVERED: [],
}


class ShipmentService:
    def __init__(
        self,
        repository: ShipmentRepository,
        db: Session,
    ):
        self.repository = repository
        self.db = db

    def create_shipment(self, data) -> Shipment:
        try:
            existing = self.repository.get_by_tracking_number(
                data.tracking_number
            )

            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="Tracking number already exists",
                )

            shipment = Shipment(
                tracking_number=data.tracking_number,
                customer_name=data.customer_name,
                origin=data.origin,
                destination=data.destination,
                status=ShipmentStatus.CREATED,
            )

            self.repository.create(shipment)
            self.db.commit()
            self.db.refresh(shipment)

            return shipment

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Shipment conflicts with existing data",
            ) from exc

        except Exception:
            self.db.rollback()
            raise

    def get_shipment(self, shipment_id: int) -> Shipment:
        shipment = self.repository.get_by_id(shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found",
            )

        return shipment

    def list_shipments(
        self,
        page: int,
        page_size: int,
        status: ShipmentStatus | None = None,
    ):
        return self.repository.list_shipments(
            page=page,
            page_size=page_size,
            status=status,
        )

    def update_status(
        self,
        shipment_id: int,
        new_status: ShipmentStatus,
    ) -> Shipment:
        try:
            shipment = self.repository.get_by_id(shipment_id)

            if shipment is None:
                raise HTTPException(
                    status_code=404,
                    detail="Shipment not found",
                )

            current_status = shipment.status

            allowed = ALLOWED_TRANSITIONS.get(
                current_status, []
            )

            if new_status not in allowed:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Cannot change status from "
                        f"{current_status.value} to "
                        f"{new_status.value}"
                    ),
                )

            history = ShipmentStatusHistory(
                shipment_id=shipment.id,
                old_status=current_status,
                new_status=new_status,
                changed_by="system",
            )

            shipment.status = new_status

            self.repository.save_status_history(history)

            self.db.commit()
            self.db.refresh(shipment)

            return shipment

        except Exception:
            self.db.rollback()
            raise