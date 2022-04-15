import pytest
import helper
import requests
import time
import buy_cheaper


MAJE_ITEM_URL   = "https://fr.maje.com/fr/pret-a-porter/collection/robes/robes-courtes/222roxanne/MFPRO02345.html"
NOT_HANDLED_URL = "https://www.amazon.fr/"

@pytest.fixture(scope="module", autouse=True)
def clean_files():
    helper.deleteDirsAndFiles("generated/*.*")

def test_retrieve_brand_item_should_return_article_price_from_MAJE_url():
    expected_price = 255.0

    item = buy_cheaper.retrieve_brand_item(MAJE_ITEM_URL)

    assert expected_price == item.price

def test_retrieve_brand_item_should_return_article_currency_from_MAJE_url():
    expected_currency = "€"

    item = buy_cheaper.retrieve_brand_item(MAJE_ITEM_URL)

    assert expected_currency == item.currency


def test_retrieve_brand_item_should_throw_error_if_domain_not_handled():
    have_throw_error = False
    
    try :
        buy_cheaper.retrieve_brand_item(NOT_HANDLED_URL)
    except NotImplementedError:
        have_throw_error = True

    assert have_throw_error


def test_update_json_file_should_init_a_new_json_file_with_item_price(request):
    json_path = f"generated/{request.node.name}.json"
    expected_price = 255.0
    expected_url = "url"
    expected_currency = "€"
    item = mockItem(expected_price, expected_url, expected_currency)

    buy_cheaper.update_json_file(item, json_path)

    json_file = helper.load_json(json_path)

    assert expected_url         == json_file["url"]
    assert expected_price       == json_file["initial_price"]
    assert expected_currency    == json_file["currency"]
    assert expected_price       == json_file["checked"][0]["price"]


def test_update_json_file_should_update_json_file_if_it_already_exist(request):
    json_path = f"generated/{request.node.name}.json"
    item = mockItem(price=255.0)
    buy_cheaper.update_json_file(item, json_path)

    item = mockItem(price=255.0)
    buy_cheaper.update_json_file(item, json_path)

    json_file = helper.load_json(json_path)

    assert 2 == len(json_file["checked"])

def test_checked_json_node_must_be_sorted_from_most_recent_to_older(request):
    json_path = f"generated/{request.node.name}.json"
    itemFirstCheck = mockItem(price=255.0)
    buy_cheaper.update_json_file(itemFirstCheck, json_path)

    itemSecondCheck = mockItem(price=230.0)
    buy_cheaper.update_json_file(itemSecondCheck, json_path)

    json_file = helper.load_json(json_path)

    assert 2 == len(json_file["checked"])
    assert json_file['checked'][0]['date'] == itemSecondCheck.date.strftime(buy_cheaper.DATE_FORMAT)
    assert json_file['checked'][0]['price'] == 230.0

    assert json_file['checked'][1]['date'] == itemFirstCheck.date.strftime(buy_cheaper.DATE_FORMAT)
    assert json_file['checked'][1]['price'] == 255.0


def test_update_json_file_should_fill_difference_and_difference_percent_update_if_price_lower_than_previous_check(request):
    json_path = f"generated/{request.node.name}.json"
    itemFirstCheck = mockItem(price=255.0)
    buy_cheaper.update_json_file(itemFirstCheck, json_path)

    itemSecondCheck = mockItem(price=230.0)
    buy_cheaper.update_json_file(itemSecondCheck, json_path)

    json_file = helper.load_json(json_path)

    assert json_file['checked'][0]['difference'] == -25.0
    assert json_file['checked'][0]['difference_percent'] == -9.8


def mockItem(price, url="this is a url", currency=None):
    item = buy_cheaper.Item(requests.Response())
    item.url = url
    item.price = price
    item.currency = currency
    return item