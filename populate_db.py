from mongoengine import connect
from models import Author, Quote
import json

connect("your_mongodb_uri")

with open("authors.json", "r") as f:
    authors_data = json.load(f)

with open("quotes.json", "r") as f:
    quotes_data = json.load(f)