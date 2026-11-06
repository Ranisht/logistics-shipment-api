from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field
from app.models.shipment import ShipmentStatus 

class ShipmentCreate(BaseModel):
    tracking_number: str = Field(
        min_length=3,
        max_length=50,
    )
    customer_name: str = Field(
        min_length=1,
        max_length=100,
    )
    origin: str = Field(min_length=1, max_length=150)
    destination: str = Field(min_length=1, max_length=150)

class ShipmentStatusUpdate(BaseModel):
    status:ShipmentStatus

class ShipmentResponse(BaseModel):
    id: int
    tracking_number: str
    customer_name: str
    origin: str
    destination: str
    status: ShipmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class ShipmentListResponse(BaseModel):
    items: list[ShipmentResponse]
    total: int
    page: int
    page_size: int