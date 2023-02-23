import telebot
from telebot import types
from dotenv import load_dotenv, find_dotenv
from db import Database
import os
import requests
import json
import numpy
from bs4 import BeautifulSoup as bs
import pandas as pd
from random_movie import random_comedy
from get_funny_holiday import random_holiday


load_dotenv(find_dotenv()) 
token = os.environ.get("TOKEN")
admin_id = int(os.environ.get("ADMIN_ID"))
weather_key = os.environ.get("WEATHER_API")

database_name = 'database'

bot = telebot.TeleBot(token)
db = Database(database_name)

@bot.message_handler(commands=['start'])
def start(message):
    print("\n\n", message,"\n\n")
    if not db.user_exist(message.from_user.id):
        if message.from_user.username != None:
            db.add_user(message.from_user.id, "@"+message.from_user.username)
    bot.send_message(message.chat.id, f'<b>Hello, {message.from_user.first_name}!</b>', parse_mode="html")

@bot.message_handler(commands=['sendto'])
def sendto(message):
    text = message.text[8:].strip().split(" ")
    user = text[0]
    mail = (' ').join(text[1:])
    if len(mail) == 0:
        bot.send_message(message.chat.id, f'Твоє повідомлення пусте, спробуй ще раз', parse_mode='html')
    user_id = db.get_user_by_username(user)
    if user_id != -1:
        bot.send_message(user_id, f'Тобі повідомлення від @{message.from_user.username}: {mail}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'Вибач, але {user} ще зі мною не вдрузях і я не можу йому надіслати твоє повідомлення <b>(ಥ﹏ಥ)</b>\nРозкажи йому про мене <b>(* ^ ω ^)</b>', parse_mode='html')



@bot.message_handler(commands=['sendall'])
def sendall(message):
    users = db.get_all()
    if message.chat.id == admin_id:
        mail = message.text[8:]
        for user in users:
            bot.send_message(user[0], mail, parse_mode="html")
    print('all messages were sent')

@bot.message_handler(commands=['answer'])
def answer(message):
    answer_text = f"From @{message.from_user.username}: "
    answer_text += message.text[7:]
    bot.send_message(admin_id, answer_text, parse_mode="html")
    print(f'admin took message from @{message.from_user.username}')


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.chat.id == admin_id:
        print("bot will be stopped in few seconds")
        cancel = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Бай бай", reply_markup=cancel)
        bot.stop_polling()
    else:
        bot.send_message(message.chat.id, "Неа, не выйдет, выключить меня может только мой хозяин)")


@bot.message_handler(commands=['weather'])
def weather(message):
    with open('cities_for_weather.json', 'r') as openfile:
        cities = json.load(openfile)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_dnipro = types.KeyboardButton("Дніпро")
    btn_kyiv = types.KeyboardButton("Київ")
    cancel = types.KeyboardButton("Відмінити")
    markup.add(btn_dnipro, btn_kyiv, cancel)
    bot.send_message(message.chat.id, text="{0.first_name}, обери місто в якому хочеш дізнатись погоду. Якщо цього міста у списку немає, то просто відправ мені його назву українською або англійською".format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['comedy'])
def comedy(message):
    cancel = telebot.types.ReplyKeyboardRemove()
    movie = random_comedy()
    bot.send_message(message.chat.id, text=f"Можу запропонувати тобі:\n<b>{movie[0]}</b> ({movie[1]})\n{movie[2]}", reply_markup=cancel, parse_mode="html")


@bot.message_handler(commands=['prazdnik'])
def holiday(message):
    cancel = telebot.types.ReplyKeyboardRemove()
    holiday_=random_holiday()
    bot.send_message(message.chat.id, text=f"{holiday_}", reply_markup=cancel, parse_mode="html")


@bot.message_handler(content_types=['text'])
def weather_cast(message):
    
    if(message.text[0] == "/"):
        return
    elif(message.text == "Відмінити"):
        cancel = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Ну може пізніше", reply_markup=cancel)
        return
    # else:
    #     cancel = telebot.types.ReplyKeyboardRemove()
    #     bot.send_message(message.chat.id, text="Прикол, не треба писати сюди будь-що", reply_markup=cancel)
    #     return
    url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_key}&units=metric'
    response = requests.get(url, params={'lang':'ua'})
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    # temperature = weather_data
    # print(temperature)
    print(weather_data)
    print(description)

    cancel = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text=f"Погода в місті {message.text}: {int(numpy.around(temperature, decimals=0))}°C також {description}", reply_markup=cancel)





bot.polling(non_stop=True)