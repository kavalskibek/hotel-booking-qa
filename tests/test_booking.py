import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../generated"))
import booking_pb2
from confluent_kafka import Consumer
import json
import time
import uuid


consumer = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'qa-test',
    'auto.offset.reset': 'earliest',
})

def test_create_booking(booking_stub):

    request = booking_pb2.CreateBookingRequest(
        user_id="user-123",
        hotel_id="hotel-001",
        room_id="room-001",
        check_in = '2026-06-06',
        check_out = '2026-06-07',
        guests = 6,
        total_price=7,
    )

    response = booking_stub.CreateBooking(request)

    assert response.status == 'PENDING'
    assert response.guests == 6


def test_get_booking(booking_stub):
    request = booking_pb2.CreateBookingRequest(
        user_id="user-123",
        hotel_id="hotel-001",
        room_id="room-001",
        check_in='2026-06-06',
        check_out='2026-06-07',
        guests=6,
        total_price=7,
    )

    response = booking_stub.CreateBooking(request)
    user_id = response.user_id

    request_get =  booking_pb2.GetBookingRequest(booking_id=response.booking_id)

    response2 = booking_stub.GetBooking(request_get)


def test_booking_kafka_event(booking_stub):
    request = booking_pb2.CreateBookingRequest(
        user_id="user-kafka-test",
        hotel_id="hotel-001",
        room_id="room-001",
        check_in="2026-07-01",
        check_out="2026-07-05",
        guests=2,
        total_price=300,
    )
    response = booking_stub.CreateBooking(request)
    booking_id = response.booking_id

    time.sleep(2)

    consumer = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': f'qa-test-{uuid.uuid4()}',
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe(['booking.created'])

    found = False
    deadline = time.time() + 15
    while time.time() < deadline:
        msg = consumer.poll(timeout=1.0)
        if msg and not msg.error():
            event = json.loads(msg.value())
            if event.get("booking_id") == booking_id:
                found = True
                break

    consumer.close()
    assert found, f"Event for booking {booking_id} not found in Kafka"