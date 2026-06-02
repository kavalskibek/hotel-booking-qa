import requests
import pytest



@pytest.mark.parametrize('guests, expected_status', [
    (1, 201),
    (0, 400),
    (-1,400),
    (10, 201),
])
def test_booking_edge_cases(register_user, guests, expected_status):
    url = 'http://localhost:8080/bookings'
    headers = {"Authorization": f"Bearer {register_user['token']}"}

    payload = {
        "hotel_id": "hotel-001",
        "room_id": "room-001",
        "check_in": "2026-10-10",
        "check_out": "2026-10-11",
        "guests": guests,
        "total_price": 100
    }
    response = requests.post(url, json=payload,headers=headers)
    assert response.status_code == expected_status

