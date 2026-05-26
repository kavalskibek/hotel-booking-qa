import grpc
import pytest
import psycopg2
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

import booking_pb2_grpc
import search_pb2_grpc
import payment_pb2_grpc

load_dotenv()

@pytest.fixture(scope="session")
def booking_stub():
    host = os.getenv("BOOKING_GRPC_HOST", "localhost")
    port = os.getenv("BOOKING_GRPC_PORT", "50051")
    channel = grpc.insecure_channel(f"{host}:{port}")
    yield booking_pb2_grpc.BookingServiceStub(channel)
    channel.close()

@pytest.fixture(scope="session")
def search_stub():
    host = os.getenv("SEARCH_GRPC_HOST", "localhost")
    port = os.getenv("SEARCH_GRPC_PORT", "50052")
    channel = grpc.insecure_channel(f"{host}:{port}")
    yield search_pb2_grpc.SearchServiceStub(channel)
    channel.close()

@pytest.fixture(scope="session")
def payment_stub():
    host = os.getenv("PAYMENT_GRPC_HOST", "localhost")
    port = os.getenv("PAYMENT_GRPC_PORT", "50053")
    channel = grpc.insecure_channel(f"{host}:{port}")
    yield payment_pb2_grpc.PaymentServiceStub(channel)
    channel.close()

@pytest.fixture(scope="session")
def db():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        database=os.getenv("POSTGRES_DB", "hotel_booking"),
        user=os.getenv("POSTGRES_USER", "qa"),
        password=os.getenv("POSTGRES_PASSWORD", "qa123"),
    )
    yield conn
    conn.close()

@pytest.fixture
def db_cursor(db):
    cur = db.cursor()
    yield cur
    db.rollback()
    cur.close()