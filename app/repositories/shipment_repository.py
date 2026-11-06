from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.shipment import Shipment, ShipmentStatus


class ShipmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, shipment_id: int) -> Shipment | None:
        statement = select(Shipment).where(
            Shipment.id == shipment_id
        )
        return self.db.scalar(statement)

    def get_by_tracking_number(
        self, tracking_number: str
    ) -> Shipment | None:
        statement = select(Shipment).where(
            Shipment.tracking_number == tracking_number
        )
        return self.db.scalar(statement)

    def create(self, shipment: Shipment) -> Shipment:
        self.db.add(shipment)
        self.db.flush()
        return shipment

    def list_shipments(
        self,
        page: int,
        page_size: int,
        status: ShipmentStatus | None = None,
    ) -> tuple[list[Shipment], int]:
        statement = select(Shipment)
        count_statement = select(func.count()).select_from(
            Shipment
        )

        if status is not None:
            statement = statement.where(
                Shipment.status == status
            )
            count_statement = count_statement.where(
                Shipment.status == status
            )

        total = self.db.scalar(count_statement) or 0

        statement = (
            statement
            .order_by(Shipment.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())
        return items, total

    def save_status_history(self, history) -> None:
        self.db.add(history)
        self.db.flush()