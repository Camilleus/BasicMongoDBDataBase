import pika
from mongoengine import connect
from models import Contact

connect("your_mongodb_uri")