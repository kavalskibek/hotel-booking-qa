import uuid

import pytest
from confluent_kafka import Consumer
from faker import Faker
from pydantic import BaseModel
import  requests
import faker
from typing import List

from tests.test_booking import consumer


class HealthHotel(BaseModel):
    status: str
    service: str





def test_get_health():
    url = 'http://localhost:8080/health'
    response = requests.get(url)
    assert response.status_code == 200

    data = HealthHotel(**response.json())
    assert data.status == 'ok'
    assert data.service == 'api-gateway'


class HotelItem(BaseModel):
    hotel_id: str
    name: str
    city: str

class SearchResponse(BaseModel):
    hotels: List[HotelItem]
    total: int

@pytest.mark.parametrize('city, check_in, check_out, guests', [
    ('Paris', '2026-07-01', '2026-07-05', 2),
    ('Barcelona', '2026-08-01', '2026-08-05', 1),
])
def test_search_hotel(city, check_in, check_out, guests):

    url = 'http://localhost:8080/hotels'
    response = requests.get(url, params={'city': city, 'check_in': check_in, 'check_out': check_out})
    assert response.status_code == 200

    data = SearchResponse(**response.json())
    assert data.total > 0
    assert data.hotels[0].city == city


def test_create_hotel(register_user):


    faker = Faker()
    url = 'http://localhost:8080/bookings'
    payload = {
        'user_id': faker.uuid4(str),
        'hotel_id': 'hotel-001',
        'room_id': 'room-001',
        'check_in': '2026-10-10',
        'check_out': '2026-10-11',
        'guests': 2,
        'total_price': 250.0
    }
    consumer = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': f'qa-test-{uuid.uuid4()}',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['booking.created'])
    headers = {'Authorization': f'Bearer {register_user['token']}'}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 201
    consumer.close()