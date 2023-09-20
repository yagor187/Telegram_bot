import get_data
from telebot import types

def calc(message, dict_data, bot):
    if dict_data["position"] == "Drips":
        drips = round(((dict_data["beans"])/ dict_data["roasting"] * dict_data["dollar"] * dict_data["weight"]/1000  + 3.05 + 2.47040  + (dict_data["film"]*(2.04/500))  + 0.13 + 0.4 + 0.28) * dict_data["count"] + dict_data["pack"], 2)
        n = drips
        n1 = round(drips * 1.1, 2)
        n2 = round(drips * 2.2, -1)
        n3 = round(drips * 3.5, -1)
        drips_str = f"Себестоимость - {n}\nУчетная цена - {n1}\nДилер - {n2}\nРРЦ - {n3}\n"
        bot.send_message(message.chat.id, drips_str.replace(".", ","))
    elif dict_data["position"] == "Capsules":
        capsules = round((dict_data["beans"] / dict_data["roasting"] * dict_data["dollar"])* 0.055 + 14.631 + 45.32 + 0.4 + dict_data["pack"], 2)
        n = capsules
        n1 = round(capsules * 1.1, 2)
        n2 = round(capsules * 1.8,-1)
        n3 = round(capsules * 2.8, -1)
        capsules_str = f"Себестоимость - {n}\nУчетная цена - {n1}\nДилер - {n2}\nРРЦ - {n3}\n"
        bot.send_message(message.chat.id, capsules_str.replace(".", ","))
    else:
        beans = round((dict_data["beans"] / dict_data["roasting"] * dict_data["dollar"]) * (dict_data["weight"])+ 14.46 + dict_data["pack"], 2)
        n = beans
        n1 = round(beans * 1.1, 2)
        n2 = round(beans * 1.45, -1)
        n3 = round(beans * 2.1, -1)
        beans_str = f"Себестоимость - {n}\nУчетная цена - {n1}\nДилер - {n2}\nРРЦ - {n3}\n"
        bot.send_message(message.chat.id,  beans_str.replace(".", ","))
    continue_1(message, bot)

def continue_1(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Хотите продолжить?", reply_markup=markup)
    bot.register_next_step_handler(message, end, bot)

def end(message, bot):
    if message.text in "Да":
        get_data.start(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начать")
        markup.add(btn1)
        bot.send_message(message.chat.id, "До завтра!", reply_markup=markup)
        bot.register_next_step_handler(message, start_again)

def start_again(message):
    get_data.start(message)





