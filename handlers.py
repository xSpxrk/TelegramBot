from loader import sql, bot, dp
from aiogram import types
from config import *
import requests
from keyboard import menu
from aiogram.dispatcher.filters import Text
from loader_templates import load_user_template, load_greeting_template, load_weather_template


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    user = message.from_user
    id = user['id']
    username = user['username']
    is_bot = user['is_bot']
    first_name = user['first_name']
    last_name = user['last_name']
    if not sql.user_exists(id):
        sql.add_user(id, username, is_bot, first_name, last_name)

    await message.reply(load_greeting_template(username, BOT_NAME))


@dp.message_handler(content_types=types.ContentType.STICKER)
async def take_message(message: types.Message):
    """
    This is echo sticker handler
    """
    file_id = getattr(message, 'sticker').file_id
    user_id = message.from_user.id
    await bot.send_sticker(user_id, file_id)


def is_admin(username):
    return username == ADMIN_USERNAME


@dp.message_handler(commands=['send_to_everyone'])
async def send_to_everyone(message: types.Message):
    """
    This is command to send users message
    """
    if is_admin(message.from_user.username):
        lst = sql.get_users_id()
        string = 'Test message'
        for i in lst:
            await bot.send_message(i[0], string)
    else:
        await message.reply('You are not admin')


def get_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather'
    units = 'metric'
    city = 'Omsk'
    params = {'q': city, 'appid': API_KEY, 'units': units}
    weather = requests.get(url, params).json()
    temp = weather['main']['temp']
    feels_like = weather['main']['feels_like']
    wind = weather['wind']['speed']
    return [temp, feels_like, wind]


@dp.message_handler(commands=['weather'])
async def send_weather(message: types.Message):
    """
    Get weather
    """
    weather = get_weather()
    res = load_weather_template(weather[0], weather[1], weather[2])
    await bot.send_message(message.from_user.id, res)


@dp.message_handler(commands=['location'])
async def send_location(message: types.Message):
    """
    Get location by coordinates
    """
    latitude, longitude = message.get_args().split(',')
    await bot.send_location(message.from_user.id, latitude, longitude)


@dp.message_handler(commands=['open_keyboard'])
async def open_keyboard(message: types.Message):
    await message.answer("Keyboard is opened", reply_markup=menu)


@dp.message_handler(Text(equals='close keyboard'))
async def close_keyboard(message: types.Message):
    await message.answer("Keyboard is closed", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['me'])
async def get_user_information(message: types.Message):
    user = message.from_user
    await message.answer(load_user_template(user['first_name'], user['last_name'], user['username'], user['id']))