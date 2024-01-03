import pika
from mongoengine import connect
from models import Contact


connect("your_mongodb_uri")


def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.fullname} at {contact.email}")
    contact.sent_email = True
    contact.save()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()