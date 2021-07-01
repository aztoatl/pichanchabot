#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import random
import sqlite3
import time
import os
import requests
import logging
import sys

HOMEDIR = './'
DB = 'responses.db'
#you can export the variable as an environment variable or just replace os.environ.get('API_KEY')  with the apikey (don't forget the "")
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)
conn = sqlite3.connect(DB, check_same_thread=False)
date = time.strftime("%I:%M:%S")
logging.basicConfig(filename='pichancha.log', level=logging.ERROR)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Konichiwa, usen /pichancha para insultos /zelda para guardar los insultos y /pack para bajar la db, /dado para un dadito")

#this funtion will return the databasefile
@bot.message_handler(commands=['pack'])
def command_hadouken(message):
    cid = message.chat.id
    bot.send_document(cid, open(DB, 'rb'))

#This will return a random number
@bot.message_handler(commands=['dice', 'bukowsky', 'dado', 'roll'])
def command_dice(message):
    if "bukowski" in message.text:
        bot.reply_to(message, "https://www.dropbox.com/s/cr63340clohuy1z/rollin.webm?dl=0")
    else:
        dice = str(random.randint(1, 100))
        bot.reply_to(message, "Tu dado es: "+dice)

#the message for the creator
@bot.message_handler(commands=['damian', 'damina', 'Damian', 'Damina', 'veggie'])
def command_damian(message):
    bot.reply_to(message, "Amo y redentor, titan de titanes, el zorro audaz, dios del humor escatologico")

#this function inserts a new response to the DB
@bot.message_handler(commands=['zelda'])
def zelda(message):
    zelda = message.text.replace("/zelda", " ").encode('latin1')
    if len(zelda) < 140:
        c = conn.cursor()
        c.execute('insert OR REPLACE into  respuestas(AnswField) values(?)', (zelda.decode('unicode-escape'),))
        print(zelda)
        conn.commit()
        c.close()
        bot.reply_to(message, "haz guardado "+zelda.decode('latin1'))
    else:
        bot.reply_to(message, "bajale a de wevos tu mensaje no me cabe en el orto")

#this is the main functionallity depending of the value will make a different thing
@bot.message_handler(commands=['pichancha', 'martin', 'twitpadrote', 'tuca'])
def responde(message):
    #if oraculo will return a yes or no response based in a random value
    if "oraculo" in message.text:
        num = random.randint(1,100)
        suerte = num % 2
        if suerte == 0:
            bot.reply_to(message, "PichaOraCulo dice: A wevo")
        else:
            bot.reply_to(message, "PichaOraCulo dice: Nel a la verga")
    else:
        c = conn.cursor()
        while True:
            #this return a random reponse from the DB
            asnwer = c.execute('select  AnswField from respuestas order by random() limit 45').fetchall()
            try:
                randum = random.randint(1, 40)
                resp = asnwer[randum]
                bot.reply_to(message, resp)
                logging.info("message sent")
                logging.info(date)
                logging.info(resp)
            except UnicodeError as e:
                #if the unicode braks the function will be added to this table to make cleanup in future
                logging.info("bad message")
                c.execute('insert OR REPLACE into  badans(answer) values(?)', (resp,))
                if resp:
                    resp = "empty"
                    logging.info(date)
                    logging.info(resp)

            break
        c.close()
        time.sleep(15)

#this will post a file just in case a NSFW content  is in the chat
# @bot.message_handler(commands=['shell', 'al', 'escudo'])
# def escudito(message):
#     cid = message.chat.id
#     img = HOMEDIR+'escudo/safe.png'
#     bot.send_photo(cid, open( img, 'rb'))

@bot.message_handler(commands=['shell', 'al', 'escudo'])
def escudito(message):
    for i in range(1,100):
        bot.reply_to(message,"soyculo")
    


def main():
    while True:
        try:
            print("Buenos dias")
            logging.info(date)
            logging.info('Started')
            bot.polling(none_stop=False)

        except requests.exceptions.ConnectionError as e:
            print(sys.stderr, str(e))
            logging.ERROR(date)
            logging.ERROR('crashed')
            logging.ERROR(str(e))
        logging.ERROR(date)
        logging.ERROR('Finished')
        print("Buenas noches")


if __name__ == '__main__':
    main()
