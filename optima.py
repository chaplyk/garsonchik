#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests

s = requests.Session()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'cookie': 'PHPSESSID=pj42rd7d60v5hn18eo3u7q4jj7; _ga=GA1.2.365212614.1542729134; _gid=GA1.2.1171649137.1543497998',
    }

s.get('https://optima.fm/uk/taxi-lviv', headers=headers)


def optima_estimate(dep_street, dep_house, arr_street, arr_house):
    global s
    # set addresses
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'cookie': 'PHPSESSID=pj42rd7d60v5hn18eo3u7q4jj7; _ga=GA1.2.365212614.1542729134; house=' + dep_house + '; _gid=GA1.2.1171649137.1543497998; street=' + dep_street + '; _gat=1',
    }

    data = {
      'address': arr_street,
      'house': arr_house,
      'type': ''
    }

    s.post('https://online.optima.taxi/settings/address-to', headers=headers, data=data)

    # get price
    response = s.post('https://online.optima.taxi/orders/cost', headers=headers).json()
    price=str(response['order_cost'])
    return price
    #"Message":"Неверно сформирован маршрут."


def get_optima_details(lat,lng):
    global s
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'cookie': 'PHPSESSID=pj42rd7d60v5hn18eo3u7q4jj7; _ga=GA1.2.365212614.1542729134; _gid=GA1.2.1171649137.1543497998',
    }

    params = (
        ('lat', lat),
        ('lng', lng),
    )

    response = s.get('https://online.optima.taxi/site/addresses/', headers=headers, params=params).json()
    street=response['geo_streets']['geo_street'][0]['name']
    house_num=str(response['geo_streets']['geo_street'][0]['houses'][0]['house'])
    return street, house_num
