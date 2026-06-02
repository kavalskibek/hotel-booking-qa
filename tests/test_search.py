import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../generated"))
import search_pb2
import pytest

@pytest.mark.regression
def test_get_hotel(search_stub):
    request = search_pb2.GetHotelRequest(hotel_id="hotel-001")
    response = search_stub.GetHotel(request)
    assert response.name == "Grand Palace Hotel"
    assert response.stars == 5