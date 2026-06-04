import uuid
import json
import requests
from confluent_kafka import Consumer
from config import BASE_URL
from helpers.kafka import consume_event

from pydantic import BaseModel

class BookingCreatedEvent(BaseModel):
    booking_id: str
    hotel_id: str
    status: str

def test_kafka_consumer(register_user, kafka_consumer):
    headers = {"Authorization": f'Bearer {register_user['token']}'}
    payload = {
        "hotel_id": "hotel-001",
        "room_id": "room-001",
        "check_in": "2026-10-10",
        "check_out": "2026-10-11",
        "guests": 1,
        "total_price": 100
    }

    response = requests.post(f'{BASE_URL}/bookings', json=payload, headers=headers)
    assert response.status_code == 201
    booking_id = response.json()['booking_id']

    event = consume_event(kafka_consumer, 'booking.created', booking_id)

    booking_event = BookingCreatedEvent(**event)
    assert booking_event.booking_id == booking_id
    assert booking_event.hotel_id == "hotel-001"

