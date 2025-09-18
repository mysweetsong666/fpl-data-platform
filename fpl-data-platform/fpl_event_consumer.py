# fpl_event_consumer.py
import pika
import json
import sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue='fpl_events')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(" [x] Received event:")
        print(json.dumps(data, indent=2))

        if data["event_type"] == "fetch_complete":
            print(" ✅ Triggering analytics pipeline...")

    channel.basic_consume(queue='fpl_events', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for events. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
