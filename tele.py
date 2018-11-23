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

DEPARTURE, ARRIVAL, TEST = range(3)

def start(bot, update):
    update.message.reply_text('Привіт! Надішли мені адресу відправлення або геолокацію:')
    return DEPARTURE

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
    update.message.reply_text('А тепер точку прибуття.')
    return ARRIVAL

def button(bot, update):
    query = update.callback_query
#    user_data['dep_street_name']=query.data
    bot.edit_message_text(text="Обрана адреса відправлення: " +  "\nБудинок: " + "\nА тепер точку прибуття.",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def arr_location(bot, update, user_data):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Точку прибуття обрано.')
    return TEST

def test(bot, update, user_data):
    user = update.message.from_user
    update.message.reply_text('Номер будинку відправлення: {} \nБільше я нічого не вмію.'.format(user_data['dep_house_number']))
#    user_data.clear()
    return ConversationHandler.END

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

            ARRIVAL: [MessageHandler(Filters.location, arr_location, pass_user_data=True)],

            TEST: [MessageHandler(Filters.text, test, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(conversation_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
