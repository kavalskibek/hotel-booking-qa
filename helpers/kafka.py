import json
import time





def consume_event(consumer, topic, booking_id, timeout=30):
    consumer.subscribe([topic])
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = consumer.poll(timeout=1.0)
        if msg and not msg.error():
            event = json.loads(msg.value().decode('utf-8'))
            if event.get('booking_id') == booking_id:
                return event
    return None