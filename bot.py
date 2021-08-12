import os
import types

import requests
import json

from telebot import TeleBot, types

token = os.environ.get("TOKEN")
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"Hello {first_name} !!")
    bot.send_message(chat_id, "With this bot you can get weather information in the city you need.")
    bot.send_message(chat_id, "Write the name of the city :")


@bot.message_handler(func=lambda m: True)
def weather(message):
    chat_id = message.chat.id
    city_name = message.text
    params = {
        'q': f'{city_name}',
        'appid': 'd316f85b72aa7669c75a4ea3238150c9'
    }
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params)
    response_json = response.json()

    try:
        country = response_json['sys']['country']
        main_description = response_json['weather'][0]['main']
        description = response_json['weather'][0]['description']

        with open('data.json', mode='w')as file:
            json.dump(response_json, file, indent=4)

        temp = str(round((float(response_json['main']['temp']) - 32) * 5 / 9 / 10, 2))
        feels_like = str(round((float(response_json['main']['feels_like']) - 32) * 5 / 9 / 10, 2))

        humidity = response_json['main']['humidity']
        clouds = response_json['clouds']['all']
        wind = response_json['wind']['speed']

        message = f"""Today in the city {city_name.capitalize()}, {country}
{main_description}: {description}
Temperature : {temp} C
Feels like : {feels_like} C
Humidity : {humidity} %
Clouds : {clouds} %
Wind : {wind} m/sek
"""
        bot.send_message(chat_id, message)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        key_save = types.KeyboardButton(text='Save')
        key_discard = types.KeyboardButton(text='Discard')
        keyboard.row(key_save, key_discard)
        question = "May I save the city name?"
        bot.send_message(chat_id, text=question, reply_markup=keyboard)
        bot.register_next_step_handler(message, save_city)

    except:
        bot.send_message(chat_id, "Unavailable city Please check and reenter !")


def save_city(message):
    pass

bot.polling(none_stop=True)
