import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

API_TOKEN = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = 'Прівіт, радий тебе бачити!\n\n' \
            'Якщо ти хочеш дізнатися, що я вмію, то напиши /help'
    await message.reply(text)

    
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Я бот для навчання Python. Поки що я вмію тільки це.")


@dp.message_handler(content_types=['photo'])    
async def photo_handler(message: types.Message):
    print(message.photo)
    await message.reply_photo(message.photo[-1].file_id)
    

    
@dp.message_handler()
async def echo(message: types.Message):
    print(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

