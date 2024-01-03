import pika
from mongoengine import connect
from models import Contact
import json
import faker


connect("your_mongodb_uri")


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


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue')