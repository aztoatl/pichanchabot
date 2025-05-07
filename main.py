#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import random
import mysql.connector
import time
import os
import requests
import logging
import sys

HOMEDIR = './'
# you can export the variable as an environment variable or just replace os.environ.get('API_KEY') with the apikey
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', ''),
    'database': os.environ.get('DB_NAME', 'shadowbo_pichancha')
}

conn = mysql.connector.connect(**db_config)
date = time.strftime("%I:%M:%S")
logging.basicConfig(filename='pichancha.log', level=logging.ERROR)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Konichiwa, usen /pichancha para insultos /zelda para guardar los insultos y /pack para bajar la db, /dado para un dadito")


@bot.message_handler(commands=['pack'])
def command_hadouken(message):
    cid = message.chat.id
    bot.send_message(cid, "Base de datos ahora en MariaDB, no disponible como archivo local.")


@bot.message_handler(commands=['dice', 'bukowsky', 'dado', 'roll'])
def command_dice(message):
    if "bukowski" in message.text:
        bot.reply_to(message, "https://www.dropbox.com/s/cr63340clohuy1z/rollin.webm?dl=0")
    else:
        dice = str(random.randint(1, 100))
        bot.reply_to(message, "Tu dado es: " + dice)


@bot.message_handler(commands=['damian', 'damina', 'Damian', 'Damina', 'veggie'])
def command_damian(message):
    bot.reply_to(message, "Amo y redentor, titan de titanes, el zorro calvo y audaz, dios del humor escatologico")


@bot.message_handler(commands=['zelda'])
def zelda(message):
    zelda = message.text.replace("/zelda", " ").encode('latin1')
    if len(zelda) < 140:
        c = conn.cursor()
        c.execute('REPLACE INTO respuestas (AnswField) VALUES (%s)', (zelda.decode('unicode-escape'),))
        conn.commit()
        c.close()
        bot.reply_to(message, "haz guardado " + zelda.decode('latin1'))
    else:
        bot.reply_to(message, "bajale a de wevos tu mensaje no me cabe en el orto")


@bot.message_handler(commands=['pichancha', 'martin', 'twitpadrote', 'tuca'])
def responde(message):
    if "oraculo" in message.text:
        num = random.randint(1, 100)
        suerte = num % 2
        if suerte == 0:
            bot.reply_to(message, "PichaOraCulo dice: A wevo")
        else:
            bot.reply_to(message, "PichaOraCulo dice: Nel a la verga")
    else:
        c = conn.cursor()
        c.execute('SELECT AnswField FROM respuestas ORDER BY RAND() LIMIT 45')
        asnwer = c.fetchall()
        try:
            randum = random.randint(1, min(40, len(asnwer) - 1))
            resp = asnwer[randum][0]
            bot.reply_to(message, resp)
            logging.info("message sent")
            logging.info(date)
            logging.info(resp)
        except Exception as e:
            logging.info("bad message")
            logging.error(str(e))
            c.execute('REPLACE INTO badans (answer) VALUES (%s)', (str(resp),))
        c.close()
        time.sleep(15)


@bot.message_handler(commands=['shell', 'al', 'escudo'])
def escudito(message):
    for i in range(1, 100):
        bot.reply_to(message, "soyculo")


def main():
    while True:
        try:
            print("Buenos dias")
            logging.info(date)
            logging.info('Started')
            bot.polling(none_stop=False)
        except requests.exceptions.ConnectionError as e:
            print(sys.stderr, str(e))
            logging.error(date)
            logging.error('crashed')
            logging.error(str(e))
        logging.error(date)
        logging.error('Finished')
        print("Buenas noches")


if __name__ == '__main__':
    main()
