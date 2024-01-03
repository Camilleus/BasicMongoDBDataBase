from mongoengine import connect
from models import Author, Quote
import re

connect("your_mongodb_uri")