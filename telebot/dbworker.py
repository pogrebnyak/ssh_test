# -*- coding: utf-8 -*-

import config
import sqlite3
from re import *

def get_state(user_id):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM base WHERE user_id=?", (user_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO base VALUES (null, ?, '0', '0', '0', '0', '0', '1')", (user_id,))
        conn.commit()
        conn.close()
        return 1
    else:
        cursor.execute("SELECT status FROM base WHERE user_id=?", (user_id,))
        text = cursor.fetchone()
        conn.close()
        return text[0]


def decorate(func):
    def wrapper(user_id, value, status):
        global cursor
        conn = sqlite3.connect(config.db_file)
        cursor = conn.cursor()
        func(user_id, value, status)
        conn.commit()
        conn.close()
    return wrapper

@decorate
def save_name_value(user_id, value, status):
    cursor.execute("UPDATE base SET name=?, status=? WHERE user_id=?", (value, status, user_id))

@decorate
def save_phone_value(user_id, value, status):
    cursor.execute("UPDATE base SET phone=?, status=? WHERE user_id=?", (value, status, user_id))

@decorate
def save_email_value(user_id, value, status):
    cursor.execute("UPDATE base SET email=?, status=? WHERE user_id=?", (value, status, user_id))

@decorate
def save_address_value(user_id, value, status):
    cursor.execute("UPDATE base SET address=?, status=? WHERE user_id=?", (value, status, user_id))

@decorate
def save_wish_value(user_id, value, status):
    cursor.execute("UPDATE base SET wish=?, status=? WHERE user_id=?", (value, status, user_id))


def check_value(value,pattern):
     is_valid = pattern.match(value)
     return True if is_valid else False

def del_all(user_id):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM base WHERE user_id=?", (user_id, ))
    conn.commit()
    conn.close()
    
S_START = '1'
S_NAME = '2'
S_PHONE = '3'
S_EMAIL = '4'
S_ADDRESS = '5'
S_WISH = '6'
S_END = '7'

email_pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
phone_pattern = compile('(^((8|\+3)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$)')


