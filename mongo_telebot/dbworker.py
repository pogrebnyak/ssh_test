# -*- coding: utf-8 -*-

from mongoengine import *
import config
from re import *

class Telebase(Document):
    user_id = LongField(unique=True)
    name = StringField()
    phone = StringField()
    email = StringField()
    address = StringField()
    wish = StringField()
    status = IntField()


def get_state(user_id):
    connect('db_telebot')
    if Telebase.objects(user_id=user_id):
        telebot_obj = Telebase.objects.get(user_id=user_id)
        return telebot_obj.status
    else:
        telebot_obj = Telebase(user_id=str(user_id), status=1).save()
        return 0

def save_name_value(user_id, value, status):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.update(name=value, status=status)

def save_phone_value(user_id, value, status):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.update(phone=value, status=status)

def save_email_value(user_id, value, status):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.update(email=value, status=status)

def save_address_value(user_id, value, status):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.update(address=value, status=status)

def save_wish_value(user_id, value, status):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.update(wish=value, status=status)

def check_value(value,pattern):
     is_valid = pattern.match(value)
     return True if is_valid else False

def del_all(user_id):
    telebot_obj = Telebase.objects.get(user_id=user_id)
    telebot_obj.delete()
    
S_START = 1
S_NAME = 2
S_PHONE = 3
S_EMAIL = 4
S_ADDRESS = 5
S_WISH = 6
S_END = 7

email_pattern = compile('(^|\s)[-A-Za-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
phone_pattern = compile('(^((8|\+3)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$)')
