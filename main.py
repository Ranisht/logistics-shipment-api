from fastapi import FastAPI
from app.api.v1.endpoints.router import api_router

app = FastAPI(
    title="Logistics Shipment Management API",
    version="1.0.0",
    description=(
        "API for managing shipments, tracking numbers, "
        "shipment status transitions and status history."
    ),
)


@app.get("/")
def root():
    return {
        "message": "Logistics Shipment Management API is running"
    }


app.include_router(api_router)
