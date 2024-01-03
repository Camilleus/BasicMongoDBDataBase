from mongoengine import connect
from models import Author, Quote, Contact
import re

connect("your_mongodb_uri")

def search_quotes(query):
    if query.startswith("name:"):
        author_name = query.split(":")[1].strip()
        authors = Author.objects(fullname__icontains=author_name)
        quotes = Quote.objects(author__in=authors)
    elif query.startswith("tag:"):
        tag_name = query.split(":")[1].strip()
        quotes = Quote.objects(tags__icontains=tag_name)
    elif query.startswith("tags:"):
        tags = query.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
    else:
        return []

    return quotes