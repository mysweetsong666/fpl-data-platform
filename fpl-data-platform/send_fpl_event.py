# send_fpl_event.py
import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="fpl_events")


event = {
    "event_type": "fetch_complete",
    "source": "collect_fpl_data",
    "timestamp": "2025-09-17T15:00:00Z",
    "note": "FPL data fetch completed"
}

channel.basic_publish(
    exchange="",
    routing_key="fpl_events",
    body=json.dumps(event)
)

print("[x] Sent fetch_complete event")

connection.close()
