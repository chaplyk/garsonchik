#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def uklon_estimate():
    data = {
      'CityId': '5',
      'route.routePoints[0].AddressName': 'Zerova street',
      'route.routePoints[0].HouseNumber': '26',
      'route.routePoints[1].AddressName': 'Городоцька вулиця',
      'route.routePoints[1].HouseNumber': '102',
      'CarType': 'Standart'
    }

    r = requests.post('https://www.uklon.com.ua/api/v1/orders/cost', headers={'client_id': '6289de851fc726f887af8d5d7a56c635'}, data=data).json()

    recommended=r['cost']
    minimal=r['cost_low']
    return minimal

print uklon_estimate()
