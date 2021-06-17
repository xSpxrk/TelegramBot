import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID, BOT_NAME
from jinja2 import Template

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    username = message.from_user.username
    id = message.from_user.id
    template = Template("Hello {{ name }}!\nI'm {{ bot_name }}\n{{ id }}")

    await message.reply(template.render(name=username, bot_name=BOT_NAME, id=id))


@dp.message_handler(content_types=types.ContentType.STICKER)
async def take_message(message: types.Message):
    """
    This is echo sticker handler
    """
    file_id = getattr(message, 'sticker').file_id
    user_id = message.from_user.id
    await bot.send_sticker(user_id, file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)