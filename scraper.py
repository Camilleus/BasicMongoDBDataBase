import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    quotes_url = "/page/1"
    all_quotes = []


    return all_quotes

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()