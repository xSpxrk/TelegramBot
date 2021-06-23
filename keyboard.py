from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True)
test = KeyboardButton('close keyboard')
menu.insert(test)
