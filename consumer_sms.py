import pika
import json
from mongoengine import connect
from models import Contact


def handle_sms_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        contact_id = message.get("contact_id")
        if contact_id:
            pass
    except Exception as e:
        print(f"Error processing SMS message")