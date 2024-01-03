from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
from models import Author, Quote
import json


with connect("mongodb+srv://CamilleusRex:<c47UaZGmGSlIR5PB>@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
    with open("authors.json", "r") as f:
        authors_data = json.load(f)

    with open("quotes.json", "r") as f:
        quotes_data = json.load(f)
        
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()
        
    for quote_data in quotes_data:
        author_fullname = quote_data["author"]
        author = Author.objects(fullname=author_fullname).first()
        quote_data["author"] = author
        quote = Quote(**quote_data)
        quote.save()
