from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
import redis 
from models import Author, Quote, Contact
import re
import json


with connect("mongodb+srv://CamilleusRex:<c47UaZGmGSlIR5PB>@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):


    def search_quotes(query):
        if re.match(r'^name:[a-z]{2}', query):
            author_name = query.split(":")[1].strip()
            authors = Author.objects(fullname__icontains=author_name)
            quotes = Quote.objects(author__in=authors)
        elif re.match(r'^tag:[a-z]{2}', query):
            tag_name = query.split(":")[1].strip()
            quotes = Quote.objects(tags__icontains=tag_name)
        elif re.match(r'^tags:[a-z,]+', query):
            tags = query.split(":")[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
        else:
            return []

        return quotes


    with redis.StrictRedis(host='localhost', port=6379, db=0) as redis_client:
        def search_quotes_with_cache(query):
            cached_result = redis_client.get(query)
            if cached_result:
                return json.loads(cached_result)
            else:
                result = search_quotes(query)
                redis_client.setex(query, 300, json.dumps(result))
                return result


        while True:
            user_input = input("Your Task: ")
            if user_input.lower() == "exit":
                break
            else:
                result = search_quotes(user_input)
                for quote in result:
                    print(quote.quote)
