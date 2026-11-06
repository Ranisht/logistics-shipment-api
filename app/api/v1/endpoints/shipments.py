from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.common import get_db
from app.models.shipment import ShipmentStatus
from app.repositories.shipment_repository import (
    ShipmentRepository,
)
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentResponse,
    ShipmentListResponse,
    ShipmentStatusUpdate,
)
from app.services.shipment_service import ShipmentService

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"],
)

DbSession = Annotated[Session, Depends(get_db)]


def get_shipment_service(db: DbSession) -> ShipmentService:
    return ShipmentService(
        repository=ShipmentRepository(db),
        db=db,
    )


ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]


@router.post(
    "",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shipment(
    request: ShipmentCreate,
    service: ShipmentServiceDep,
):
    return service.create_shipment(request)


@router.get(
    "/{shipment_id}",
    response_model=ShipmentResponse,
)
def get_shipment(
    shipment_id: int,
    service: ShipmentServiceDep,
):
    return service.get_shipment(shipment_id)


@router.get(
    "",
    response_model=ShipmentListResponse,
)
def list_shipments(
    service: ShipmentServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    shipment_status: ShipmentStatus | None = Query(
        default=None,
        alias="status",
    ),
):
    items, total = service.list_shipments(
        page=page,
        page_size=page_size,
        status=shipment_status,
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.put(
    "/{shipment_id}/status",
    response_model=ShipmentResponse,
)
def update_shipment_status(
    shipment_id: int,
    request: ShipmentStatusUpdate,
    service: ShipmentServiceDep,
):
    return service.update_status(
        shipment_id=shipment_id,
        new_status=request.status,
    )