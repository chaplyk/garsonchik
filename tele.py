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
    update.message.reply_text('Привіт! Надішли мені адресу відправлення:')
    return DEPARTURE

def uklon_address(street_name):
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

def dep_address(bot, update):
    global dep_house_number
    street_name=re.sub("\d*$", "", update.message.text)
    dep_house_number=update.message.text.replace(street_name, "")
    reply_markup = InlineKeyboardMarkup(uklon_address(street_name))
    update.message.reply_text('Обери із переліку:', reply_markup=reply_markup)
    update.message.reply_text('А тепер адресу прибуття.')
    return ARRIVAL

def dep_location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('А тепер адресу прибуття.')
    return ARRIVAL

def button(bot, update):
    global street
    query = update.callback_query
    street=format(query.data)
    bot.edit_message_text(text="Обрана адреса відправлення: " + street + "\nБудинок: " + dep_house_number + "\nА тепер адреса прибуття.",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def arr_location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Точку прибуття обрано.')
    return TEST

def test(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Я більше нічого не вмію.')

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
            DEPARTURE: [MessageHandler(Filters.text, dep_address),
            MessageHandler(Filters.location, dep_location)],

            ARRIVAL: [MessageHandler(Filters.location, arr_location)],

            TEST: [MessageHandler(Filters.text, test)]
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
