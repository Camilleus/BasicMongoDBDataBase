from mongoengine import connect
import redis 
from models import Author, Quote, Contact
import re
import json


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


while True:
    user_input = input("Your Task: ")
    if user_input.lower() == "exit":
        break
    else:
        result = search_quotes(user_input)
        for quote in result:
            print(quote.quote)
            
            
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def search_quotes_with_cache(query):
    cached_result = redis_client.get(query)
    if cached_result:
        return json.loads(cached_result)
    else:
        result = search_quotes(query)
        redis_client.setex(query, 300, json.dumps(result))
        return result