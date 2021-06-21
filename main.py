import logging
from aiogram import Bot, Dispatcher, executor, types
from config import *
from jinja2 import Environment, FileSystemLoader
from Sql import SQL
import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
sql = SQL('db')


def load_greeting_template(name, bot_name):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('greeting.txt')
    return template.render(name=name, bot_name=bot_name)


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
    if username == ADMIN_USERNAME:
        return True
    return False


@dp.message_handler(commands=['test'])
async def send_message_to_users(message: types.Message):
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


def load_weather_template(temp, feels_like, wind):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('weather.txt')
    return template.render(temp=temp, feels_like=feels_like, wind=wind)


def get_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather'
    units = 'metric'
    city = 'Omsk'
    params = {'q': city, 'appid': API_KEY, 'units': units}
    weather = requests.get(url, params)
    weather = weather.json()
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


@dp.message_handler(commands=['get_location'])
async def send_location(message: types.Message):
    """
    Get location by coordinates
    """
    latitude, longitude = message.get_args().split(',')
    await bot.send_location(message.from_user.id, latitude, longitude)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
