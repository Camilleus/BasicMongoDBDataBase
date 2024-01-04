from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
import redis
from models import Author, Quote, Contact
import re
import json
from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query):
        pass

class NameSearch(SearchStrategy):
    def search(self, query):
        author_name = query.split(":")[1].strip()
        authors = Author.objects(fullname__icontains=author_name)
        quotes = Quote.objects(author__in=authors)
        return quotes

class TagSearch(SearchStrategy):
    def search(self, query):
        tag_name = query.split(":")[1].strip()
        quotes = Quote.objects(tags__icontains=tag_name)
        return quotes

class TagsSearch(SearchStrategy):
    def search(self, query):
        tags = query.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        return quotes

class SearchContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_search(self, query):
        return self.strategy.search(query)

def search_quotes(user_input, search_context):
    result = search_context.execute_search(user_input)
    for quote in result:
        print(quote.quote)

if __name__ == "__main__":
    redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
        user_input = input("Your Task: ")
        if user_input.lower() == "exit":
            break
        else:
            if re.match(r'^name:[a-z]{2}', user_input):
                strategy = NameSearch()
            elif re.match(r'^tag:[a-z]{2}', user_input):
                strategy = TagSearch()
            elif re.match(r'^tags:[a-z,]+', user_input):
                strategy = TagsSearch()
            else:
                print("Invalid command")
                continue

            search_context = SearchContext(strategy)
            search_quotes(user_input, search_context)

    redis_cache.close()
