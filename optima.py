#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

dep_street='ЗЕРОВА ВУЛ.'
dep_house='16'

# SET ADDRESSES
headers = {
#    'authority': 'online.optima.taxi',
#    'cache-control': 'max-age=0',
#    'origin': 'https://online.optima.taxi',
#    'upgrade-insecure-requests': '1',
#    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#    'referer': 'https://online.optima.taxi/settings/address-to',
#    'accept-encoding': 'gzip, deflate, br',
#    'accept-language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
    'cookie': 'PHPSESSID=pj42rd7d60v5hn18eo3u7q4jj7; _ga=GA1.2.365212614.1542729134; house=' + dep_house + '; _gid=GA1.2.1171649137.1543497998; street=' + dep_street + '; _gat=1',
}

data = {
  'address': 'УГОРСЬКА ВУЛ.',
  'house': '20',
  'type': ''
}

response1 = requests.post('https://online.optima.taxi/settings/address-to', headers=headers, data=data)

# GET THE COST
#headers = {
#    'cookie': 'PHPSESSID=pj42rd7d60v5hn18eo3u7q4jj7; _ga=GA1.2.365212614.1542729134; house=' + dep_house + '; _gid=GA1.2.1171649137.1543497998; _gat=1; street=' + dep_street,
#    'origin': 'https://online.optima.taxi',
#    'accept-encoding': 'gzip, deflate, br',
#    'accept-language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
#    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#    'accept': 'application/json, text/javascript, */*; q=0.01',
#    'referer': 'https://online.optima.taxi/',
#    'authority': 'online.optima.taxi',
#}

response = requests.post('https://online.optima.taxi/orders/cost', headers=headers)

print response.text
