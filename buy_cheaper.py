
import requests
import helper
from os.path import exists
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse


DATE_FORMAT = "%d/%m/%Y, %H:%M:%S"

class Item:
    url = None
    date = None
    soup = None
    price = None
    currency = None
    difference = None
    difference_percent = None

    def __init__(self, response):
        self.url = response.url
        self.date = datetime.now()
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.retrieve_price()
        self.retrieve_currency()

    def retrieve_price(self):
        pass

    def retrieve_currency(self):
        pass

    
    def get_json_item_initialisation(self):
        json_item = {}
        json_item["url"] = self.url
        json_item["initial_price"] = self.price
        if self.currency is not None : json_item["currency"] = self.currency
        json_item["checked"] = [self.get_checked_json_item()]
        
        return json_item
    
    def get_checked_json_item(self):
        json_item = {}
        json_item["date"] = self.date.strftime(DATE_FORMAT)
        json_item["price"] = self.price
        if self.difference is not None : json_item["difference"] = self.difference
        if self.difference_percent is not None: json_item["difference_percent"] = self.difference_percent 

        return json_item

class Maje(Item):
    def __init__(self, response):
        super().__init__(response)

    def retrieve_price(self):
        self.price = float(self.soup.find(attrs={"itemprop": "price"})["content"])

    def retrieve_currency(self):
        price_with_currency = self.soup.find(attrs={"itemprop": "price"}).contents[0]
        self.currency = price_with_currency[-1]


def retrieve_brand_item(url):
    domain = urlparse(url).netloc
    response = requests.get(url)

    if "maje" in domain:
        return Maje(response)
    else:
        raise NotImplementedError(f"domain [{domain}] parser not implemented")


def update_json_file(item : Item, json_file_path):

    if not exists(json_file_path):
        json = item.get_json_item_initialisation()

    else:
        json = helper.load_json(json_file_path)
        update_item_with_difference(json["initial_price"], item)
        json["checked"].insert(0, item.get_checked_json_item())

    helper.write_json(json, json_file_path)


def update_item_with_difference(initial_price, item : Item):
    print(f"\n item.price {item.price}")
    print(f"\n initial_price {initial_price}")
    
    if item.price != initial_price:
        item.difference = item.price - initial_price
        item.difference_percent = round((item.difference * 100) / initial_price, 1)
        print(f"\n Not the same price, difference is {item.difference}, it represent {item.difference_percent}%")
 
