import requests
from config import BASE_URL
import psycopg2


# conn = psycopg2.connect(
#     host='localhost',
#     database='hotel_booking',
#     user='qa',
#     password='qa123'
# )
#
#
#
# cur = conn.cursor()
# cur.execute('SELECT * FROM bookings Where booking_id = %s', (booking_id))
#
# row = cur.fetchone()
# assert row is not None  # запись существует



def test_payment_success(register_user):
    url = 'http://localhost:8080/bookings'
    headers = {"Authorization": f"Bearer {register_user['token']}"}

    payload = {
        "hotel_id": "hotel-001",
        "room_id": "room-001",
        "check_in": "2026-10-10",
        "check_out": "2026-10-11",
        "guests": 2,
        "total_price": 100
    }
    response = requests.post(f'{BASE_URL}/bookings', json=payload, headers=headers)
    assert response.status_code == 201

    booking_id = response.json()['booking_id']

    payment_payload = {
        "booking_id": booking_id,
        "amount": 100.0,
        "currency": "usd",
        "token": "tok_visa"
    }
    payment_response = requests.post(f"{BASE_URL}/payments", json=payment_payload, headers=headers)
    assert payment_response.status_code == 201
    assert payment_response.json()["status"] == "SUCCESS"

    conn = psycopg2.connect(
        host = 'localhost',
        database = 'hotel_booking',
        user = 'qa',
        password = 'qa123'
    )
    curr = conn.cursor()
    curr.execute('SELECT * FROM bookings Where id = %s', (booking_id,))
    row = curr.fetchone()
    assert row is not None