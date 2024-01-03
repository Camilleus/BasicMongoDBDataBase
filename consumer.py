import pika
from mongoengine import connect
from models import Contact
import json


connect("your_mongodb_uri")


def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.fullname} at {contact.email}")
    contact.sent_email = True
    contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get("contact_id")
    if contact_id:
        send_email(contact_id)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='contacts_queue')


channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()