"""
Módulo para configurações
"""
from decouple import config
from expiringdict import ExpiringDict


class Config:
    MESSAGE_SPAM_FILTER = ExpiringDict(max_len=500, max_age_seconds=30)
    TOKEN = config('TOKEN')

    MONGO_CONFIG = {
        'MONGO_HOST': config('MONGO_HOST', 'mongodb://localhost'),
        'MONGO_PORT': config('MONGO_PORT', '27017'),
        'MONGO_DATABASE': config('MONGO_DATABASE'),
        'MONGO_USER': config('MONGO_USER'),
        'MONGO_PASS': config('MONGO_PASS')
    }
