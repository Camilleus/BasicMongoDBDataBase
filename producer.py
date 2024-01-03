import pika
import json
import faker
from mongoengine import connect
from models import Contact


def generate_fake_contacts(num_contacts):
    fake = faker.Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = {
            "fullname": fake.name(),
            "email": fake.email(),
            "sent_email": False,
            "phone_number": fake.phone_number(),
            "preferred_method": fake.random_element(["email", "sms"])
        }
        contacts.append(contact)
    return contacts


with connect("mongodb+srv://CamilleusRex:<c47UaZGmGSlIR5PB>@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='contacts_queue')


    fake_contacts = generate_fake_contacts(10)


    for contact in fake_contacts:
        contact_doc = Contact(**contact)
        contact_doc.save()

        message = {"contact_id": str(contact_doc.id)}
        channel.basic_publish(exchange='', routing_key='contacts_queue', body=json.dumps(message))


    connection.close()
