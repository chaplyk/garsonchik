#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#Starting the bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, TypeHandler)
import requests
import logging
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bing_token='AlbYLa6vjKs19Iv2ygH8FfHHFNE3bg6aVseGSt0JxNtEJ6cqGw2vSFl_1vk6bffl'

DEPARTURE, ARRIVAL, TEST = range(3)

# /start command handler
def start(bot, update):
    update.message.reply_text('Привіт! Надішли мені адресу відправлення або геолокацію:')
    return DEPARTURE

# Function that parses address options from Uklon and appends them to InlineKeyboard list
def uklon_address_list(street_name):
    headers = {
        'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cookie': 'City=5'
    }
    response = requests.get('https://www.uklon.com.ua/api/v1/addresses?limit=5&q=' + street_name, headers=headers).json()
    keyboard  = []
    for a in response:
        address=a['address_name']
        keyboard.append([InlineKeyboardButton(address, callback_data=address)])
    return keyboard

# Function that gets estimated price of Uklon
def uklon_estimate(dep_street_name,dep_house_number,arr_street_name,arr_house_number):
    data = {
      'CityId': '5',
      'route.routePoints[0].AddressName': dep_street_name,
      'route.routePoints[0].HouseNumber': dep_house_number,
      'route.routePoints[1].AddressName': arr_street_name,
      'route.routePoints[1].HouseNumber': arr_house_number,
      'CarType': 'Standart'
    }

    r = requests.post('https://www.uklon.com.ua/api/v1/orders/cost', headers={'client_id': '6289de851fc726f887af8d5d7a56c635'}, data=data).json()
    recommended=r['cost']
    minimal=str(r['cost_low'])
    return minimal

# Receive address line from geolocation
"""def bing_address(latitude, longitude):
    url='http://dev.virtualearth.net/REST/v1/Locations/' + latitude + ',' + longitude + '?key=' + bing_token
    r = requests.get(url).json()
    address=r['resourceSets'][0]['resources'][0]['address']['addressLine']
    return address"""

# Receive coordinates from address
"""def bing_address(street, house_number):
    url='http://dev.virtualearth.net/REST/v1/Locations?q=' +  street + '%20' + house_number + '%20Lviv%20Ukraine&key=' + bing_token
    r = requests.get(url).json()
    geo=r['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']
    latitude=geo[0]
    longitude=geo[1]
    return address"""

# DEPARTURE state
def dep_address(bot, update, user_data):
    dep_street_name=re.sub("\d*$", "", update.message.text)
    user_data['dep_house_number'] = update.message.text.replace(dep_street_name, "")
    reply_markup = InlineKeyboardMarkup(uklon_address_list(dep_street_name))
    update.message.reply_text('Обери вулицю із переліку:', reply_markup=reply_markup)
    return ARRIVAL

def dep_location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    #print bing_geo(str(user_location.latitude), str(user_location.longitude))
    update.message.reply_text('А тепер точку прибуття.')
    return ARRIVAL

# ARRIVAL state
def arr_address(bot, update, user_data):
    arr_street_name=re.sub("\d*$", "", update.message.text)
    user_data['arr_house_number'] = update.message.text.replace(arr_street_name, "")
    reply_markup = InlineKeyboardMarkup(uklon_address_list(arr_street_name))
    update.message.reply_text('Обери вулицю із переліку:', reply_markup=reply_markup)
    return TEST

def arr_location(bot, update, user_data):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Точку прибуття обрано.')
    return TEST

# callback_query for dep_address and arr_address functions
def button(bot, update, user_data):
    query = update.callback_query
    if user_data.get('arr_house_number') is None:
        user_data['dep_street_name']=query.data
        bot.edit_message_text(text="Адреса відправлення: " + user_data['dep_street_name'] + "\nБудинок: " + user_data['dep_house_number'] + "\nА тепер точку прибуття.",
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
    if user_data.get('arr_house_number') is not None:
        user_data['arr_street_name']=query.data
        bot.edit_message_text(text="Адреса прибуття: " + user_data['arr_street_name'] + "\nБудинок: " + user_data['arr_house_number'] + "\nРозраховую вартість...",
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)

# Test function. To be removed
def test(bot, update, user_data):
    uklon=uklon_estimate(user_data['dep_street_name'],user_data['dep_house_number'],user_data['arr_street_name'],user_data['dep_house_number'])
    update.message.reply_text('Мінімальна вартість в Uklon: ' + uklon)

# /cancel command handler
def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Гарного дня!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    # Log Errors caused by Updates.
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and get the dispatcher
    updater = Updater("718020912:AAHswzgdQX-X-xO6A14b-G9J2Yh7ZhpVflE")
    dp = updater.dispatcher

    # Add conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            DEPARTURE: [MessageHandler(Filters.text, dep_address, pass_user_data=True),
            MessageHandler(Filters.location, dep_location)],

            ARRIVAL: [MessageHandler(Filters.text, arr_address, pass_user_data=True),
            MessageHandler(Filters.location, arr_location, pass_user_data=True)],

            TEST: [MessageHandler(Filters.text, test, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CallbackQueryHandler(button, pass_user_data=True))

    dp.add_handler(conversation_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
