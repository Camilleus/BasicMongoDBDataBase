import pika
from mongoengine import connect
from models import Contact
import json
import faker

connect("your_mongodb_uri")