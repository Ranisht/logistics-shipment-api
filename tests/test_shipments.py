from uuid import uuid4


def test_create_shipment(client):
    tracking_number = f"TRK_TEST_{uuid4().hex[:12].upper()}"

    response = client.post(
        "/api/v1/shipments",
        json={
            "tracking_number": tracking_number,
            "customer_name": "ABC Logistics",
            "origin": "Chennai",
            "destination": "Bengaluru",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["tracking_number"] == tracking_number
    assert data["status"] == "CREATED"