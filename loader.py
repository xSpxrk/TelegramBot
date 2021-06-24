import logging
from aiogram import Bot, Dispatcher, types
from Sql import SQL
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
sql = SQL('db')

logging.basicConfig(level=logging.INFO)