"""
Módulo dedicado à funções de conexão e operação com o banco de dados.
"""
import logging
from tiao.settings import Config
from pymongo import MongoClient

log = logging.getLogger()


def get_db():
    """
    Retorna uma conexão com mongo.
    """
    user = Config.MONGO_CONFIG['MONGO_USER']
    pwd = Config.MONGO_CONFIG['MONGO_PASS']
    host = Config.MONGO_CONFIG['MONGO_HOST']
    port = Config.MONGO_CONFIG['MONGO_PORT']

    client = MongoClient(f'mongodb://{user}:{pwd}@{host}:{port}')

    return client[Config.MONGO_CONFIG['MONGO_DATABASE']]


def get_user_data(chat_id, username):
    """
    Returns a list of user data from database.
    param : chat_id : <str>
    param : username : <str>
    """
    collection = get_db()[chat_id]

    return collection.find({'username': username})


def get_or_create_user(chat_id, username):
    """
    Verifica se é um novo usuário, se for cria o registro no banco.
    Se não retorne o objeto ja criado.
    """
    user_data = list(get_user_data(chat_id, username))

    if user_data:
        return user_data

    # Define default attributes
    user = {
        'username': username,
        'chat_id': chat_id,
        'lists': [],
        'messages': [],
    }
    db = get_db()
    user_data = db[chat_id].insert_one(user)

    return list(user_data)


def add_message(chat_id, username, message):
    """
    Atualiza mensagens enviadas por um usuario
    """
    user = next(get_or_create_user(chat_id, username), None)

    if not user:
        return False

    user['messages'].append(message)
    db = get_db()
    try:
        db[chat_id].replace_one(
            {'username': username},
            user,
            upsert=True
        )
    except:
        return False

    return True


def add_new_list(chat_id, username, list_reference):
    user = next(iter(get_or_create_user(chat_id, username)), None)

    if not user:
        return False

    new_list = {
        'reference': list_reference,
        'items': []
    }
    user['lists'].append(new_list)

    db = get_db()
    try:
        db[chat_id].replace_one(
            {'username': username},
            user,
            upsert=True
        )
    except:
        return False

    return True


def update_list(chat_id, username, list_reference, value):
    user = next(iter(get_or_create_user(chat_id, username)), None)

    if not user:
        return False

    refs = [i for i in user['lists'] if i['reference'] == list_reference]
    if not any(refs):
        return False

    for list_ in user['lists']:
        if list_['reference'] == list_reference:
            list_['items'].append(value)

    db = get_db()
    try:
        db[chat_id].replace_one(
            {'username': username},
            user,
            upsert=True
        )
    except:
        return False

    return True
