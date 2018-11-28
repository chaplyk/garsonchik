#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

bing_token='AlbYLa6vjKs19Iv2ygH8FfHHFNE3bg6aVseGSt0JxNtEJ6cqGw2vSFl_1vk6bffl'

#getting address from location
def get_address():
    url='http://dev.virtualearth.net/REST/v1/Locations/49.833201,23.993919?key=' + bing_token
    r = requests.get(url).json()
    address=r['resourceSets'][0]['resources'][0]['address']['addressLine']
    street_name=address.rsplit(',', 1)[0].replace("vulytsia", "street")
    dep_house_number=address.rsplit(',', 1)[1]
    return street_name, dep_house_number

def get_geo():
    street='Городоцька вулиця 20'
    url='http://dev.virtualearth.net/REST/v1/Locations?q=' +  street + '%20Lviv%20Ukraine&key=' + bing_token
    r = requests.get(url).json()
    geo=r['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']
    latitude=geo[0]
    longitude=geo[1]
    return latitude, longitude

print get_address()[0]
