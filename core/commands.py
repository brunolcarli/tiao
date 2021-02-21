import requests
import json
import ast
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tiao.settings import Config
from core.connection import get_user_data, add_message, add_new_list, update_list

def version(bot, update):
    """
    Pings the bot
    """
    chat_id = update.message.chat_id
    return bot.send_message(chat_id=chat_id, text='0.0.0')


def new_list(bot, update):
    """
    Creates a new list
    """
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    data = ' '.join(update.message.text.split()[1:])

    new_list = add_new_list(str(chat_id), username, data)

    if new_list:
        return bot.send_message(chat_id=chat_id, text=f'Done: Created list with ID: `{data}`')

    return bot.send_message(chat_id=chat_id, text='Sorry, try again latter...')


def lists(bot, update):
    """
    View user lists
    """
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    data = update.message.text.split()[1:]

    user_data = list(get_user_data(str(chat_id), username))

    if not user_data:
        return bot.send('This user have no data registered yet.')

    if not data:
        arrow = '\xE2\x9E\xA1'.encode('utf-8')
        lists_show = ''.join(f'\u2794 {l["reference"]}\n' for l in user_data[0]['lists'])

        return bot.send_message(chat_id=chat_id, text=lists_show)

    list_data = [i for i in user_data[0]['lists'] if i['reference'] == data[0]]
    lists_show = ''.join(f'\u2794 {i}\n' for i in list_data[0]['items'])

    if not list_data:
        return bot.send_message(chat_id=chat_id, text='This list is empty...')
    if not lists_show:
        return bot.send_message(chat_id=chat_id, text='This list is empty...')

    return bot.send_message(chat_id=chat_id, text=lists_show)


def add(bot, update):
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    data = update.message.text.split()[1:]
    if len(data) < 2:
        return bot.send_message(chat_id=chat_id, text='Expected key and value.')

    key, *value = data
    value = ' '.join(i for i in value)

    update = update_list(str(chat_id), username, key, value)
    if not update:
        return bot.send_message(chat_id=chat_id, text='sorry, try again later.')

    return bot.send_message(chat_id=chat_id, text=f'Added {value} to the list {key}')


def run():
    updater = Updater(Config.TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('version', version))
    dp.add_handler(CommandHandler('new_list', new_list))
    dp.add_handler(CommandHandler('lists', lists))
    dp.add_handler(CommandHandler('add', add))
    updater.start_polling()
    updater.idle()
