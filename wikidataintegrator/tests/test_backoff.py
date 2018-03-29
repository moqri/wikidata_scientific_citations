import unittest
import requests
import sys

from wikidataintegrator import wdi_login
from wikidataintegrator.backoff.wdi_backoff import wdi_backoff
from wikidataintegrator.wdi_config import config
from wikidataintegrator.wdi_core import WDItemEngine
pyv = sys.version_info.major
if pyv == 3:
    import json
else:
    import simplejson as json


class TestMethods(unittest.TestCase):
    def test_all(self):
        config['BACKOFF_MAX_TRIES'] = 2
        config['BACKOFF_MAX_VALUE'] = 2
        with self.assertRaises(requests.RequestException):
            bad_http_code()
        with self.assertRaises(requests.RequestException):
            bad_login()
        with self.assertRaises(requests.RequestException):
            item()

        assert good_http_code() == "200 OK"

        with self.assertRaises(json.JSONDecodeError):
            bad_json()


@wdi_backoff()
def bad_http_code():
    r = requests.get("http://httpstat.us/400")
    r.raise_for_status()
    print(r.text)


@wdi_backoff()
def good_http_code():
    r = requests.get("http://httpstat.us/200")
    r.raise_for_status()
    print(r.text)
    return r.text


@wdi_backoff()
def bad_json():
    json.loads("<xml>I failed :(</xml>")


@wdi_backoff()
def bad_request():
    requests.get("http://www.fakeurlgsdkjhjgfseg.com")


def bad_login():
    wdi_login.WDLogin("name", "pass", server="www.wikidataaaaaaaaa.org")


def item():
    wd_item = WDItemEngine(wd_item_id="Q14911732", server='www.wikidataaaaaaaaa.org', search_only=True)
    print(wd_item.get_label('en'))


if __name__ == "__main__":
    if sys.argv[1] == "json":
        bad_json()
    if sys.argv[1] == "request":
        bad_request()
    if sys.argv[1] == "login":
        bad_login()
    if sys.argv[1] == "item":
        item()
    if sys.argv[1] == "badcode":
        bad_http_code()
    if sys.argv[1] == "goodcode":
        good_http_code()
