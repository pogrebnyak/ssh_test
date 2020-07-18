from flask import Flask
from flask import request, abort, session
from telebot import types
import telebot
import os
import config
import time
from work import loto


myCmd2 = os.popen('hostname').read()

WEBHOOK_HOST = '34.77.212.75:443'
PATH = 'bot2/bot'
WEBHOOK_URL = f'{WEBHOOK_HOST}/{PATH}{config.token}'


bot = telebot.TeleBot(config.token)
keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard.row('uptime')

app = Flask(__name__)

@app.route('/')
def index():
    return f'Flask'

@app.route(f'/{PATH}{config.token}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':

        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        abort(403)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, myCmd2, reply_markup=keyboard)

@bot.message_handler(commands=["uptime"])
def cmd_uptime(message):
    upcmd = os.popen('uptime').read()
    bot.send_message(message.chat.id, upcmd)

@bot.message_handler(commands=["pegas"])
def my_pegas(message):
    bot.send_message(message.chat.id,loto(6,52))


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'uptime':
        myCmd = os.popen('uptime').read()
        myCmd = myCmd
        bot.send_message(message.chat.id, myCmd)



@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_message(message.chat.id, message.sticker.file_id)

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
             url=WEBHOOK_URL,
             certificate=open('./nginx-selfsigned.crt','r')
             )
    print(bot.get_webhook_info())
    app.run(host='127.0.0.1', port=5001, debug=True)
