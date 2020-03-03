# -*- coding: utf-8 -*-

from flask import Flask
import telebot
import config
import dbworker
import time
from flask import request, abort
from telebot import types

WEBHOOK_HOST = '31.134.121.72:8443'
PATH = 'bot'
WEBHOOK_URL = f'{WEBHOOK_HOST}/{PATH}{config.token}'

bot = telebot.TeleBot(config.token)
keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
keyboard1.row('/start','/reset')

keyboard2 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_geo = types.KeyboardButton(text='Отправить местопооложение', request_location=True)
keyboard2.add(button_geo)

app = Flask(__name__)

@app.route(f'/{PATH}{config.token}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':

        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        abort(403)

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_state(message.chat.id)
    if state == dbworker.S_START:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить своё имя, но так и не сделал этого :( Жду...")
    elif state == dbworker.S_NAME:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить свой телефон, но так и не сделал этого :( Жду...")
    elif state == dbworker.S_PHONE:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить свою почту, но так и не сделал этого :( Жду...")
    elif state == dbworker.S_EMAIL:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить свое местопооложение, но так и не сделал этого :( Жду...", reply_markup=keyboard2)
    elif state == dbworker.S_ADDRESS:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить свои пожелания, но так и не сделал этого :( Жду...")
    elif state == dbworker.S_WISH:
        bot.send_message(message.chat.id, "Я все про вас знаю:)")    #, reply_markup=keyboard3)
    else:
        bot.send_message(message.chat.id, "Привет! Введи свои ФИО", reply_markup=keyboard1)
 
@bot.message_handler(commands=['reset'])
def user_delete_all(message):
    dbworker.del_all(message.chat.id)
    bot.send_message(message.chat.id, "Удалил все. Введи /start")

@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == dbworker.S_START)
def user_entering_name(message):
    bot.send_message(message.chat.id, "Отличное имя, запомню! Теперь укажи, пожалуйста, свой телефон")
    dbworker.save_name_value(message.chat.id, message.text, dbworker.S_NAME)

@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == dbworker.S_NAME)
def user_entering_phone(message):
    if dbworker.check_value(message.text, dbworker.phone_pattern):
        bot.send_message(message.chat.id, "Спасибо! Теперь укажи, пожалуйста, свой e-mail.")
        dbworker.save_phone_value(message.chat.id, message.text, dbworker.S_PHONE)
    else:
        bot.send_message(message.chat.id, "Что-то не так, введи корректный номер телефона!")
        
@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == dbworker.S_PHONE)
def user_entering_email(message):
    if dbworker.check_value(message.text, dbworker.email_pattern):
       bot.send_message(message.chat.id, "Спасибо! Теперь отправь, пожалуйста, свое местоположение.", reply_markup=keyboard2)
       dbworker.save_email_value(message.chat.id, message.text, dbworker.S_EMAIL)
    else: 
       bot.send_message(message.chat.id, "Что-то не так, введи корректный e-mail!")

@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == dbworker.S_EMAIL, content_types=['location'])
def user_entering_address(message):
    if message.location is not None:
        bot.send_message(message.chat.id, "Спасибо! Теперь укажи, пожалуйста, свои пожелания.", reply_markup=keyboard1)
        dbworker.save_address_value(message.chat.id, f'{message.location.latitude} {message.location.longitude}', dbworker.S_ADDRESS)

@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == dbworker.S_ADDRESS)
def user_wish_address(message):
    bot.send_message(message.chat.id, "Спасибо!")
    dbworker.save_wish_value(message.chat.id, message.text, dbworker.S_WISH)


if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
             url=WEBHOOK_URL,
             certificate=open('./nginx-selfsigned.crt','r')
             )
    print(bot.get_webhook_info())
    app.run(host='127.0.0.1', port=5000, debug=True)



 



