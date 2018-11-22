#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

headers = {
    'client_id': '6289de851fc726f887af8d5d7a56c635',
}

data = {
  'CityId': '5',
  'Referer': 'https://www.uklon.com.ua/',
  'route.routePoints[0].AddressName': 'Зерова вулиця',
  'route.routePoints[0].HouseNumber': '26',
  'route.entrance': '',
  'route.comment': '',
  'IsRouteUndefined': 'false',
  'route.routePoints[1].AddressName': 'Городоцька вулиця',
  'route.routePoints[1].HouseNumber': '102',
  'TimeType': 'now',
  'CarType': 'Standart',
  'PaymentType': 'Cash',
  'PaymentInfo': 'Наличными',
  'ClientName': '',
  'Phone': '',
  'ExtraCost': '0',
  'RememberUser': 'false'
}

r = requests.post('https://www.uklon.com.ua/api/v1/orders/cost', headers=headers, data=data)

print r.text
