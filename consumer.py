from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pika
from mongoengine import connect
from models import Contact
import json
import logging


with connect("mongodb+srv://CamilleusRex:<c47UaZGmGSlIR5PB>@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):


    def send_email(contact_id):
        contact = Contact.objects.get(id=contact_id)
        print(f"Sending email to {contact.fullname} at {contact.email}")
        contact.sent_email = True
        contact.save()


    logging.basicConfig(level=logging.INFO)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            contact_id = message.get("contact_id")
            if contact_id:
                send_email(contact_id)
        except Exception as e:
            logging.error(f"Error processing message: {e}")



    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='contacts_queue')


    channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    connection.close()
