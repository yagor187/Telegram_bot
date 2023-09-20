import telebot
from telebot import types

import main
from Config import token
from Dollar import curs_dollar
from calculate import calc
import time

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["vcr"])
def start(message):
    dict_data = {
        "user_id": message.chat.id,
        "position":"", # наименование позиции
        "dollar": 0, # курс доллара
        "weight": 0, # в граммах
        "pack": 0.0, # стоимость упаковки
        "beans": 0.0, # стоимость зерна
        "roasting": "", # обжарка
        "count":None, # Количнсвто дрипов
        "cost_beans": [],
        "procent_beans":[],
        "film": 0.0
    }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Capsules")
    btn2 = types.KeyboardButton("Drips")
    btn3 = types.KeyboardButton("Beans")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=markup)
    bot.register_next_step_handler(message, select_position, dict_data)

def select_position(message, dict_data):
    dict_data["position"] = message.text
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите стоимость зерна через пробел', reply_markup=markup)
    bot.register_next_step_handler(message, beans, dict_data)

def beans(message, dict_data):
    try:
        dict_data["cost_beans"] = str(message.text).replace(",",".").split()
        dict_data["cost_beans"] = [float(i) for i in dict_data["cost_beans"]]
        bot.send_message(message.chat.id, 'Введите соотношение через пробел')
        bot.register_next_step_handler(message, procent, dict_data)
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка!Введите соотношение через пробел')
        bot.register_next_step_handler(message, beans, dict_data)

def procent(message, dict_data):
    dict_data["procent_beans"] = str(message.text).replace(",",".").split()
    dict_data["procent_beans"] = [float(i) for i in dict_data["procent_beans"]]
    if len(dict_data["procent_beans"]) != len(dict_data["cost_beans"]) or sum(dict_data["procent_beans"]) != 1.0:
        bot.send_message(message.chat.id, 'Данные введены неверно, ввдеите стоимость зерна и соотношения повторно')
        bot.register_next_step_handler(message, beans, dict_data)
    else:
        if dict_data["position"] == "Drips":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("11")
            btn2 = types.KeyboardButton("12")
            markup.add(btn1, btn2)
            bot.register_next_step_handler(message, weight, dict_data)
            bot.send_message(message.chat.id, 'Введите вес кофе в дрипе', reply_markup=markup)

        elif dict_data["position"] == "Capsules":
            bot.register_next_step_handler(message, pack, dict_data)
            bot.send_message(message.chat.id, 'Введите стоимость упаковки')
        else:
            bot.register_next_step_handler(message, weight, dict_data)
            bot.send_message(message.chat.id, 'Введите вес зерна')

        for i in range(len(dict_data["procent_beans"])):
            dict_data["beans"] += dict_data["procent_beans"][i] * dict_data["cost_beans"][i]

def weight(message, dict_data):
    try:
        markup = types.ReplyKeyboardRemove()
        message.text = str(message.text).replace(",", ".")
        dict_data["weight"] = float(message.text)
        if dict_data["position"] == "Drips":
            bot.register_next_step_handler(message, count, dict_data)
            bot.send_message(message.chat.id, 'Введите количество дрипов в упаковке', reply_markup=markup)
        else:
            bot.register_next_step_handler(message, pack, dict_data)
            bot.send_message(message.chat.id, 'Введите стоимость упаковки', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Ошибка! Введите вес повторно')
        bot.register_next_step_handler(message, weight, dict_data)

def count(message, dict_data):
    try:
        markup = types.ReplyKeyboardRemove()
        message.text = str(message.text).replace(",",".")
        dict_data["count"] = int(message.text)
        bot.register_next_step_handler(message, pack, dict_data)
        bot.send_message(message.chat.id, 'Введите стоимость упаковки', reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка!Введите стоимость упаковки')
        bot.register_next_step_handler(message, pack, dict_data, bot, types)
def pack(message, dict_data):
    try:
        message.text = str(message.text).replace(",",".")
        dict_data["pack"] = float(message.text)
        roasting(message, dict_data)
    except Exception:
        bot.send_message(message.chat.id, 'Данные стомости введены неверно, введите стоимость упаковки повторно')
        bot.register_next_step_handler(message, pack, dict_data)

def roasting(message, dict_data):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Dark")
    btn2 = types.KeyboardButton("Medium")
    markup.add(btn1, btn2)
    if dict_data["position"] == "Drips":
        bot.send_message(message.chat.id, 'Введите стоимость пленки')
        bot.register_next_step_handler(message, film, dict_data)
    else:
        bot.send_message(message.chat.id, 'Выберете обжарку', reply_markup=markup)
        bot.register_next_step_handler(message, select_roasting, dict_data)


def film(message, dict_data):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Dark")
        btn2 = types.KeyboardButton("Medium")
        markup.add(btn1, btn2)
        message.text = str(message.text).replace(",",".")
        print(message.text)
        dict_data["film"] = float(message.text)
        bot.send_message(message.chat.id, 'Выберете обжарку', reply_markup=markup)
        bot.register_next_step_handler(message, select_roasting, dict_data)
    except Exception:
        bot.send_message(message.chat.id, 'Вы ввели данные неверно, повторите попытку')
        bot.register_next_step_handler(message, film, dict_data)

def select_roasting(message, dict_data):
    if message.text in ["Dark", "Medium"]:
        if message.text in "Dark":
            dict_data["roasting"] = 0.8
        else:
            dict_data["roasting"] = 0.83
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите курс', reply_markup=markup)
        bot.register_next_step_handler(message, enter_dollar, dict_data, bot)
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно, введите повторно')
        bot.register_next_step_handler(message, select_roasting, dict_data)


def enter_dollar(message, dict_data, bot):
    if message.text == "N" or message.text == "n":
        dict_data["dollar"] = curs_dollar()
    else:
        try:
            dict_data["dollar"] = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, 'Курс доллара введен неправильно, введите повторно')
            bot.register_next_step_handler(message, enter_dollar, dict_data)
    for k, v in dict_data.items():
        print(k, v)
    calc(message, dict_data, bot)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)


