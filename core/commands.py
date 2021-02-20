import requests
import json
import ast
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tiao.settings import Config


def version(bot, update):
    """
    Pings the bot
    """
    chat_id = update.message.chat_id
    return bot.send_message(chat_id=chat_id, text='0.0.0')


def run():
    updater = Updater(Config.TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('version', version))
    updater.start_polling()
    updater.idle()
