"""
Módulo para configurações
"""
from decouple import config
from expiringdict import ExpiringDict


class Config:
    MESSAGE_SPAM_FILTER = ExpiringDict(max_len=500, max_age_seconds=30)
    TOKEN = config('TOKEN')
