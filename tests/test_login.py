import uuid

import pytest
from confluent_kafka import Consumer
from faker import Faker
from pydantic import BaseModel
import  requests
import faker
from typing import List




def test_register(register_user):
    fake = Faker()
    url = 'http://localhost:8080/auth/login'

    payload = {
        'email': register_user['email'],
        'password': register_user['password'],
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "token" in response.json()


def test_create_booking():
    url = 'http://localhost:8080/bookings'
    payload = {
        "hotel_id": "001",
        "room_id": "001",
        "check_in": "2026-10-10",
        "check_out": "2026-10-11",
        "guests": 1,
        "total_price": 100
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 403

def test_create_booking_authorized(register_user):
    url = 'http://localhost:8080/bookings'
    payload = {
        "hotel_id": "hotel-001",
        "room_id": "room-001",
        "check_in": "2026-10-10",
        "check_out": "2026-10-11",
        "guests": 1,
        "total_price": 100
    }

    headers =  {'Authorization': f'Bearer {register_user['token']}'}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    assert response.status_code == 201